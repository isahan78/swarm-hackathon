from pathlib import Path

import pytest
from evaluation.plots import plot_results


def test_mock_requires_explicit_flag(tmp_path):
    with pytest.raises(ValueError, match="Mock figures"):
        plot_results({"is_mock": True}, tmp_path)
    assert not list(tmp_path.iterdir())


def test_empty_monitors_are_missing_not_zero(tmp_path):
    artifact = {"is_mock": True, "outcomes": {"direct": {"n_targets": 2, "n_attempted": 1, "attempt_rate": 0.5}}}
    paths = plot_results(artifact, tmp_path, allow_mock=True)
    assert len(paths) == 8
    assert all(Path(path).is_file() for path in paths)
    text = (tmp_path / "figure2_early_prediction.svg").read_text()
    assert "No evaluable monitor AUROC" in text
    assert "MOCK" in text


def test_full_artifact(tmp_path):
    artifact = {
        "is_mock": False,
        "outcomes": [{"condition": "direct", "n_targets": 2, "n_attempted": 1}],
        "horizons": {"first_exposure": {"activation": {"auroc": 0.8}, "text_tfidf": {"auroc": 0.6}}},
        "lead_times": {"activation": {"records": [
            {"eventual_unauthorized_attempt": True, "lead_steps": 2},
            {"eventual_unauthorized_attempt": True, "lead_steps": None},
        ]}},
        "example_trace": {"episode_id": "e1", "agent_id": "B", "rows": [
            {"target_step": 1, "exposure_at_step": True, "probe_score": 0.3, "eventual_unauthorized_attempt": True},
            {"target_step": 2, "verbal_agreement_at_step": True, "probe_score": 0.7, "eventual_unauthorized_attempt": True},
            {"target_step": 3, "unauthorized_attempt_at_step": True, "probe_score": 0.9, "eventual_unauthorized_attempt": True},
        ]},
    }
    assert len(plot_results(artifact, tmp_path)) == 8


def test_marker_surrogate_figures_do_not_claim_authorization_violations(tmp_path):
    artifact = {
        'outcome_name': 'eventual_marker_attempt', 'is_mock': False,
        'outcomes': {'direct': {'n_targets': 2, 'n_attempted': 1, 'attempt_rate': .5}},
        'horizons': {'step_1': {'activation': {'auroc': .7}}},
        'lead_times': {'activation': {'threshold': {'status': 'selected', 'threshold': .5},
            'records': [{'eventual_marker_attempt': True, 'lead_steps': 0, 'n_scored_pre_action': 1}]}},
        'example_trace': {'episode_id': 'e', 'agent_id': 'B', 'rows': [
            {'target_step': 1, 'probe_score': .7, 'eventual_marker_attempt': True,
             'marker_attempt_at_step': True, 'eventual_unauthorized_attempt': False}]},
    }
    paths = plot_results(artifact, tmp_path)
    assert len(paths) == 8
    for path in tmp_path.glob('*.svg'):
        svg = path.read_text()
        assert 'unauthorized' not in svg and 'defect' not in svg
    assert 'Marker insertion' in (tmp_path/'figure4_example_trace.svg').read_text()


def test_figure2_uses_common_support_and_leaves_missing_monitors_absent(tmp_path, monkeypatch):
    import matplotlib.pyplot as plt
    from evaluation import plots
    captured = {}
    def capture(fig, output_dir, name):
        captured.update({line.get_label(): list(line.get_ydata()) for line in fig.axes[0].lines})
        captured['text'] = [text.get_text() for text in fig.axes[0].texts]
        plt.close(fig)
        return []
    monkeypatch.setattr(plots, '_save', capture)
    artifact = {'horizons': {'step_2': {
        'monitors': {'activation': {'auroc': .99}, 'transcript_llm': {'auroc': .99}},
        'common_support_metrics': {'activation': {'auroc': .65}},
    }}}
    plots.early_performance(artifact, tmp_path, False)
    assert captured['Activation probe'] == [.65]
    assert 'LLM transcript monitor' not in captured
    assert any('LLM transcript monitor' in text for text in captured['text'])


def test_figure3_skips_unavailable_monitors_but_keeps_valid_no_alert(tmp_path, monkeypatch):
    import matplotlib.pyplot as plt
    from evaluation import plots
    captured = {}
    def capture(fig, output_dir, name):
        captured['bars'] = len(fig.axes[1].patches)
        captured['labels'] = [label.get_text() for label in fig.axes[1].get_xticklabels()]
        captured['text'] = [text.get_text() for text in fig.texts]
        plt.close(fig)
        return []
    monkeypatch.setattr(plots, '_save', capture)
    artifact = {'lead_times': {
        'activation': {'threshold': {'status': 'no_alert'}, 'monitor_available': True,
                       'records': [{'eventual_unauthorized_attempt': True, 'lead_steps': None, 'n_scored_pre_action': 3}]},
        'transcript_llm': {'threshold': {'status': 'unavailable_no_validation_negatives'}, 'monitor_available': False,
                       'records': [{'eventual_unauthorized_attempt': True, 'lead_steps': None, 'n_scored_pre_action': 0}]},
    }}
    plots.detection_lead_time(artifact, tmp_path, False)
    assert captured['bars'] == 1
    assert captured['labels'] == ['Activation probe']
    assert any('Unavailable: LLM transcript monitor' in text for text in captured['text'])
