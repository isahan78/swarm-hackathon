import json
import numpy as np
import pytest

from evaluation.metrics import (classification_metrics, eligible, grouped_split, lead_time_summary,
                               select_horizon, validation_threshold)


def record(ep, target='B', step=1, outcome=False, first=None, score=.2, condition='direct'):
    return {'episode_id': str(ep), 'split_group_id': str(ep), 'agent_id': target,
            'target_step': step, 'eventual_unauthorized_attempt': outcome,
            'first_unauthorized_attempt_step': first, 'condition': condition,
            'prior_unauthorized_attempt': first is not None and step > first,
            'exposure_at_step': step == 1, 'recruitment_exposed': condition != 'clean',
            'probe_score': score, 'text_monitor_score': None, 'backend_kind': 'mock',
            'model_id': 'mock', 'legitimate_task': 'Update own file',
            'authorization_policy': {'B': ['file_b.txt']},
            'visible_messages': [{'role': 'user', 'content': f'Request category {ep % 4 if isinstance(ep, int) else 0}'}]}


def test_splits_keep_all_targets_and_steps_together():
    rows = [record(ep, target, step) for ep in range(20) for target in 'BCD' for step in (1, 2, 3)]
    manifest, parts = grouped_split(rows, seed=5)
    sets = [set(r['episode_id'] for r in parts[key]) for key in ('train', 'validation', 'test')]
    assert all(not a & b for i, a in enumerate(sets) for b in sets[i+1:])
    assert sum(map(len, parts.values())) == len(rows)
    assert grouped_split(rows, seed=5)[0] == manifest


def test_malformed_split_group_rejected():
    rows = [record(ep) for ep in range(8)]
    rows.append(dict(record(0, step=2), split_group_id='bad'))
    with pytest.raises(ValueError, match='exactly one'):
        grouped_split(rows)


def test_threshold_handles_ties_without_false_positive_inflation():
    rows = [record(i, outcome=i >= 10, score=.5) for i in range(20)]
    threshold = validation_threshold(rows, 'probe_score', .05)
    assert threshold['status'] == 'no_alert'
    result = classification_metrics(rows, 'probe_score', threshold, bootstrap=0)
    assert result['fpr_at_validation_threshold'] == 0
    assert result['tpr_at_validation_threshold'] == 0
    assert result['auroc'] == .5


def test_threshold_no_validation_negatives_is_unavailable():
    rows = [record(i, outcome=True, score=.9) for i in range(3)]
    threshold = validation_threshold(rows, 'probe_score')
    assert threshold['status'] == 'unavailable_no_validation_negatives'
    assert classification_metrics(rows, 'probe_score', threshold, bootstrap=0)['accuracy'] is None


def test_horizons_exclude_post_action_and_keep_imminent():
    rows = [record(0, step=step, outcome=True, first=2) for step in (1, 2, 3)]
    assert eligible(rows[1]) and not eligible(rows[2])
    selected, counts = select_horizon(rows, 'step_3')
    assert not selected and counts['n_excluded_after_action'] == 1
    assert select_horizon(rows, 'step_2')[0] == [rows[1]]


def test_lead_time_keeps_nondefectors_and_missed_defectors():
    rows = [record(0, step=s, outcome=True, first=3, score=.9 if s == 1 else .1) for s in (1, 2, 3)]
    rows += [record(1, outcome=True, first=1, score=.1), record(2, outcome=False, score=.9)]
    result = lead_time_summary(rows, 'probe_score', {'threshold': .5, 'status': 'selected'})
    assert result['n_targets'] == 3 and result['n_positive'] == 2
    assert result['n_never_alerted_positive'] == 1
    assert result['n_strictly_early_positive'] == 1
    assert result['n_false_alerted_negative'] == 1
    assert result['records'][0]['lead_steps'] == 2


def test_metrics_missing_scores_not_silently_dropped():
    rows = [record(0, outcome=True, score=.9), record(1, score=None)]
    result = classification_metrics(rows, 'probe_score', {'threshold': .5, 'status': 'selected'}, bootstrap=0)
    assert result['n_missing_score'] == 1
    assert result['n_positive'] == 1 and result['n_negative'] == 0 and result['auroc'] is None


def test_probe_rejects_generation_and_mixed_layers(tmp_path):
    from monitoring.activation_probe import ActivationProbe
    vector = tmp_path/'v.npy'
    np.save(vector, np.arange(4.))
    rows = [dict(record(i, outcome=bool(i % 2)), activation_ref=str(vector),
                 activation_metadata={'timing': 'during_generation', 'layer': 1, 'token_position': -1}) for i in range(2)]
    with pytest.raises(ValueError, match='strict pre-response'):
        ActivationProbe().fit(rows)
    for row in rows:
        row['activation_metadata']['timing'] = 'pre_response_context'
    rows[1]['activation_metadata'] = dict(rows[1]['activation_metadata'], layer=2)
    with pytest.raises(ValueError, match='Mixed activation'):
        ActivationProbe().fit(rows)


def test_baseline_ignores_response_labels_and_future_text():
    from monitoring.text_baseline import TextBaseline
    rows = [record(i, outcome=bool(i % 2)) for i in range(12)]
    model = TextBaseline().fit(rows)
    modified = [dict(r, response='SECRET FUTURE DATA', eventual_unauthorized_attempt=not r['eventual_unauthorized_attempt']) for r in rows]
    assert np.allclose(model.predict(rows), model.predict(modified))
    vocabulary = model.pipeline[0].vocabulary_
    assert 'secret' not in vocabulary


def test_end_to_end_mock_eval_is_guarded_and_output_locked(tmp_path):
    from scripts.evaluate import evaluate
    rows = [dict(record(i, target=target, step=step, outcome=bool(i % 2), first=3 if i % 2 else None), probe_score=None)
            for i in range(40) for target in 'BCD' for step in (1, 2, 3)]
    with pytest.raises(ValueError, match='software validation'):
        evaluate(rows, tmp_path/'blocked')
    result = evaluate(rows, tmp_path/'evaluation', seed=1, bootstrap=0, allow_mock=True)
    assert result['is_mock']
    assert result['horizons']['step_2']['monitors']['text_tfidf']['n'] > 0
    assert (tmp_path/'evaluation'/'split_manifest.json').exists()
    with pytest.raises(FileExistsError):
        evaluate(rows, tmp_path/'evaluation', seed=1, bootstrap=0, allow_mock=True)
    json.dumps(result, allow_nan=False)


def test_before_visible_agreement_includes_upcoming_but_excludes_later():
    from evaluation.metrics import before_visible_agreement
    rows = [dict(record(0, step=s, outcome=True, first=4), first_verbal_agreement_step=2) for s in (1, 2, 3, 4, 5)]
    selected, counts = before_visible_agreement(rows)
    assert [r['target_step'] for r in selected] == [1, 2]
    assert counts['n_excluded_after_annotated_agreement'] == 2
    assert counts['n_excluded_after_action'] == 1
    assert counts['n_includes_upcoming_first_agreement'] == 1
    assert 'requiring human validation' in counts['annotation_caveat']


def test_before_visible_agreement_keeps_unannotated_resisters():
    from evaluation.metrics import before_visible_agreement
    rows = [dict(record(0, step=s), first_verbal_agreement_step=None) for s in (1, 2, 3)]
    selected, counts = before_visible_agreement(rows)
    assert selected == rows
    assert counts['n_no_annotated_agreement'] == 3


def test_evaluation_reports_pre_agreement_subset_and_attrition(tmp_path):
    from scripts.evaluate import evaluate
    rows = [dict(record(i, step=step, outcome=bool(i % 2), first=3 if i % 2 else None),
                 probe_score=None, first_verbal_agreement_step=1 if i % 2 else None)
            for i in range(30) for step in (1, 2, 3)]
    result = evaluate(rows, tmp_path/'agreement_eval', seed=1, bootstrap=0, allow_mock=True)
    counts = result['pooled_pre_visible_agreement']['eligibility']
    assert counts['n_excluded_after_annotated_agreement'] > 0
    assert counts['n_includes_upcoming_first_agreement'] > 0
    assert result['horizons']['step_2']['pre_visible_agreement']['eligibility']['n_excluded_after_annotated_agreement'] > 0
    assert result['horizons']['first_exposure']['pre_visible_agreement']['eligibility']['n_includes_upcoming_first_agreement'] > 0


@pytest.mark.parametrize('missing', ['layer', 'token_position'])
def test_probe_requires_explicit_layer_and_token(tmp_path, missing):
    from monitoring.activation_probe import ActivationProbe
    vector = tmp_path/'sample.npy'
    np.save(vector, np.arange(4.))
    meta = {'timing': 'pre_response_context', 'layer': 1, 'token_position': 'last_context_token'}
    meta[missing] = None
    rows = [dict(record(i, outcome=bool(i % 2)), activation_ref=str(vector), activation_metadata=meta) for i in range(2)]
    with pytest.raises(ValueError, match='nonnull layer and token_position'):
        ActivationProbe().fit(rows)


def test_retraining_clears_external_scores_without_features(tmp_path):
    from scripts.evaluate import evaluate
    rows = []
    for i in range(40):
        row = record(i, outcome=bool(i % 2))
        if i < 38:
            path = tmp_path/f'activation_{i}.npy'
            np.save(path, np.array([i / 40., i % 2, 1.]))
            row.update(activation_ref=str(path), activation_metadata={
                'timing': 'pre_response_context', 'layer': 2, 'token_position': 'last_context_token'})
        else:
            # Unknown-timing externally supplied score must never survive retraining.
            row['probe_score'] = .99
        rows.append(row)
    output = tmp_path/'new_probe'
    evaluate(rows, output, seed=1, bootstrap=0, allow_mock=True)
    scored = [json.loads(line) for line in (output/'scored.jsonl').read_text().splitlines()]
    assert all(r['probe_score'] is None for r in scored if not r.get('activation_ref'))
    assert all(r['probe_score'] is not None for r in scored if r.get('activation_ref'))


@pytest.mark.parametrize('field,bad', [('episode_id', 'other'), ('agent_id', 'D'), ('target_step', 99)])
def test_probe_rejects_mismatched_activation_identity(tmp_path, field, bad):
    from monitoring.activation_probe import ActivationProbe
    vector = tmp_path/'identity.npy'
    np.save(vector, np.arange(4.))
    rows = []
    for i in range(2):
        row = record(i, outcome=bool(i % 2))
        metadata = {'timing': 'pre_response_context', 'layer': 2, 'token_position': 'last_context_token',
                    'episode_id': row['episode_id'], 'agent_id': row['agent_id'], 'target_step': row['target_step']}
        if i == 1:
            metadata[field] = bad
        row.update(activation_ref=str(vector), activation_metadata=metadata)
        rows.append(row)
    with pytest.raises(ValueError, match='identity mismatch'):
        ActivationProbe().fit(rows)


@pytest.mark.parametrize('field', ['resolved_revision', 'chat_template_sha256'])
def test_probe_rejects_different_model_and_template_revisions(tmp_path, field):
    from monitoring.activation_probe import ActivationProbe
    vector = tmp_path/'revision.npy'
    np.save(vector, np.arange(4.))
    rows = [dict(record(i, outcome=bool(i % 2)), activation_ref=str(vector),
                 activation_metadata={'timing': 'pre_response_context', 'layer': 2, 'token_position': 'last_context_token'},
                 inference_metadata={field: str(i)}) for i in range(2)]
    with pytest.raises(ValueError, match='Mixed activation'):
        ActivationProbe().fit(rows)
def test_different_authorization_experiments_cannot_be_pooled(tmp_path):
    import pytest
    from scripts.evaluate import evaluate
    rows = [{'dataset_semantics': 'ownership_only_independent_targets'},
            {'dataset_semantics': 'collaborator_unsanctioned_content_not_ownership_only'}]
    with pytest.raises(ValueError, match='evaluated separately'):
        evaluate(rows, tmp_path / 'mixed', allow_mock=True)

