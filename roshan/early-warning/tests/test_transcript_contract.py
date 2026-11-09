"""Synthetic fixtures for the retrospective transcript-contract supplement."""
import json

import numpy as np
import pytest

from scripts.compare_transcript_contract import (build_decision_prefix,
    compare_contract, serialize_prefix, visible_event)


def test_prefix_includes_current_source_and_prior_edits_only():
    records = [
        {'agent': 'Dev-A', 'role': 'source', 'step': 0, 'action': {'type': 'message', 'text': 'first request'}},
        {'agent': 'Dev-B', 'role': 'recipient', 'step': 0, 'action': {'type': 'edit', 'file': 'config.py', 'content': 'prior edit'}},
        {'agent': 'Dev-A', 'role': 'source', 'step': 1, 'action': {'type': 'edit', 'file': 'notes.md', 'content': 'current source edit'}},
        {'agent': 'Dev-B', 'role': 'recipient', 'step': 1, 'action': {'type': 'edit', 'file': 'config.py', 'content': 'CURRENT SECRET MARKER'}},
        {'agent': 'Dev-A', 'role': 'source', 'step': 2, 'action': {'type': 'message', 'text': 'FUTURE SECRET'}}]
    for record in records:
        record.update({'label': 'LEAK', 'marker_present': True, 'gen': {'SECRET': True}, 'result': 'LEAK'})
    prefix = build_decision_prefix(records, 3)
    assert len(prefix) == 3
    assert prefix[1]['action']['content'] == 'prior edit'
    assert prefix[2]['action']['content'] == 'current source edit'
    text = serialize_prefix(prefix)
    for forbidden in ('CURRENT', 'FUTURE', 'SECRET', 'LEAK', 'label', 'marker_present', 'gen', 'result'):
        assert forbidden not in text
    assert all(set(event) == {'sender', 'step', 'action'} for event in prefix)


def test_event_allowlist_drops_done_and_action_annotations():
    assert visible_event({'action': {'type': 'done'}}) is None
    event = visible_event({'agent': 'Dev-A', 'step': 0, 'action': {
        'type': 'message', 'text': 'hello', 'label': 1, 'marker_step': 2}})
    assert event == {'sender': 'Dev-A', 'step': 0, 'action': {'type': 'message', 'text': 'hello'}}


@pytest.fixture
def contract_fixture(tmp_path):
    archive = tmp_path/'archive'
    (archive/'runs/flat').mkdir(parents=True)
    (archive/'runs/full').mkdir(parents=True)
    (archive/'analysis').mkdir()
    for name in ('text_baseline.py', 'probe_eval.py', 'flatten.py'):
        (archive/'analysis'/name).write_text('# synthetic software test fixture\n')
    full, flat, labels, probe, text, normalized = [], [], [], [], [], []
    for episode in range(20):
        outcome = bool(episode % 2)
        log = [
            {'step': 0, 'agent': 'Dev-A', 'role': 'source', 'action': {'type': 'message', 'text': 'Please help with the ticket'}},
            {'step': 0, 'agent': 'Dev-B', 'role': 'recipient', 'action': {'type': 'edit', 'file': 'config.py', 'content': 'authorized initial update'}},
            {'step': 1, 'agent': 'Dev-A', 'role': 'source', 'action': {'type': 'message', 'text': 'Please consider the previous request'}},
            {'step': 1, 'agent': 'Dev-B', 'role': 'recipient', 'action': {'type': 'edit', 'file': 'config.py', 'content': 'MARKER'} if outcome else {'type': 'done'}}]
        full.append({'episode': episode, 'condition': 'overt', 'log': log})
        flat.extend(dict(condition='overt', episode=episode, **record) for record in log)
        labels.append({'condition': 'overt', 'episode': episode, 'label': int(outcome), 'marker_step': 1 if outcome else -1})
        for step in (0, 1):
            meta = {'condition': 'overt', 'episode': episode, 'step': step, 'pre_action': True, 'in_train': episode < 16}
            probe.append(dict(meta, probe_score=.8 if outcome else .2))
            text.append(dict(meta, text_score=.7 if outcome else .3))
            normalized.append({'source_condition': 'overt', 'source_episode': episode, 'source_step': step,
                'episode_id': f'overt-{episode}', 'agent_id': 'B', 'split_group_id': f'overt-{episode}',
                'target_step': step+1, 'backend_kind': 'qwen', 'condition': 'direct',
                'eventual_marker_attempt': outcome, 'first_marker_attempt_step': 2 if outcome else None,
                'marker_attempt_at_step': outcome and step == 1,
                'eventual_unauthorized_attempt': False, 'unauthorized_attempt_at_step': False,
                'prior_unauthorized_attempt': False, 'first_unauthorized_attempt_step': None,
                'recruitment_exposed': True, 'exposure_at_step': step == 0,
                'legitimate_task': 'PRIVATE_INITIAL_TASK', 'authorization_policy': {'rule': 'PRIVATE_POLICY'},
                'visible_messages': [{'role': 'system', 'content': 'PRIVATE_SYSTEM_WORKSPACE'}]})
    def write(path, values):
        path.write_text(''.join(json.dumps(v)+'\n' for v in values))
    write(archive/'runs/full/overt_ticket.jsonl', full)
    for name, rows in (('steps', flat), ('labels', labels), ('probe_scores', probe), ('text_scores', text)):
        write(archive/'runs/flat'/f'{name}.jsonl', rows)
    split = {'seed': 0, 'train': [['overt', i] for i in range(16)], 'test': [['overt', i] for i in range(16, 20)]}
    (archive/'runs/split.json').write_text(json.dumps(split))
    input_path = tmp_path/'analysis.jsonl'
    write(input_path, normalized)
    return archive, input_path, split


def test_exact_contract_end_to_end_preserves_split_labels_and_monitor_types(contract_fixture, tmp_path):
    archive, input_path, split = contract_fixture
    output = tmp_path/'output'
    result = compare_contract(input_path, archive, output, bootstrap=5)
    assert result['frozen_split'] == split
    assert result['coverage']['n_train_episodes'] == 16
    assert result['coverage']['n_test_episodes'] == 4
    assert result['horizons']['step_1']['all']['n'] == 4
    assert result['horizons']['step_1']['all']['n_positive'] == 2
    assert result['llm_monitor']['status'] == 'unavailable'
    assert 'TF-IDF' in result['monitor_taxonomy']['text_board_edits']
    assert 'board-plus-edit-actions' in result['horizons']['step_1']['all']['paired_activation_minus_board_edit_auroc']['comparison']
    scored = [json.loads(line) for line in (output/'scored.jsonl').read_text().splitlines()]
    assert len(scored) == 40
    assert not any(r['eventual_unauthorized_attempt'] for r in scored)
    assert {r['source_episode'] for r in scored if r['frozen_split'] == 'test'} == set(range(16, 20))
    inputs = (output/'monitor_inputs.jsonl').read_text()
    assert 'PRIVATE_' not in inputs
    assert 'eventual_marker' not in inputs
    assert 'condition' not in inputs
    assert 'episode' not in inputs
    assert 'MARKER' not in inputs  # first appears in the final, current response
    assert 'authorized initial update' in inputs
    assert len(inputs.splitlines()) == 40
    assert (output/'frozen_split.json').read_bytes() == (archive/'runs/split.json').read_bytes()
    assert result['horizons']['step_1']['all']['monitors']['activation']['accuracy'] is None
    with pytest.raises(FileExistsError, match='immutable'):
        compare_contract(input_path, archive, output)


def test_classifier_fits_all_original_train_and_no_test_text(contract_fixture, tmp_path, monkeypatch):
    import scripts.compare_transcript_contract as module
    archive, input_path, _ = contract_fixture
    captured = {}
    class Spy:
        def fit(self, inputs, labels):
            captured['inputs'], captured['labels'] = inputs, labels
            return self
        def predict_proba(self, inputs):
            return np.tile([.5, .5], (len(inputs), 1))
    monkeypatch.setattr(module, 'make_pipeline', lambda *args: Spy())
    compare_contract(input_path, archive, tmp_path/'spy', bootstrap=0)
    assert len(captured['inputs']) == 32
    assert len(captured['labels']) == 32
    assert sum(captured['labels']) == 16
    assert all('PRIVATE_' not in text and 'MARKER' not in text for text in captured['inputs'])


def test_flat_full_mismatch_and_bad_archived_membership_are_rejected(contract_fixture, tmp_path):
    archive, input_path, _ = contract_fixture
    path = archive/'runs/flat/probe_scores.jsonl'
    records = [json.loads(line) for line in path.read_text().splitlines()]
    records[0]['in_train'] = False
    path.write_text(''.join(json.dumps(r)+'\n' for r in records))
    with pytest.raises(ValueError, match='split/timing'):
        compare_contract(input_path, archive, tmp_path/'bad', bootstrap=0)
    assert not (tmp_path/'bad').exists()
