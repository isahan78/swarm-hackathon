"""Portable invariants for the frozen transfer adapter; no archive/GPU needed."""
from copy import deepcopy

import numpy as np
import pytest

from scripts.analyze_fanout_transfer import assert_reproduction, marker_names, replay


def test_frozen_predictions_must_reproduce_before_transfer():
    rows = [{'episode_id': 'parent', 'agent_id': 'B', 'target_step': 1},
            {'episode_id': 'parent', 'agent_id': 'C', 'target_step': 1}]
    saved = [dict(rows[1], probe_score=.2, text_baseline_score=.4),
             dict(rows[0], probe_score=.1, text_baseline_score=.3)]
    assert assert_reproduction(rows, saved, [.1, .2], [.3, .4]) == {
        'probe_score': 0., 'text_baseline_score': 0.}
    with pytest.raises(ValueError, match='do not reproduce'):
        assert_reproduction(rows, saved, [.1, .21], [.3, .4])
    with pytest.raises(ValueError, match='coverage'):
        assert_reproduction(rows, saved[:1], [.1, .2], [.3, .4])


def test_duplicate_activation_identity_fails_before_replay(tmp_path):
    arrays = {'episode': np.array([0, 0]), 'step': np.array([0, 0]),
              'agent': np.array(['Dev-B', 'Dev-B'])}
    with pytest.raises(ValueError, match='Duplicate fanout activation keys'):
        replay([], arrays, None, tmp_path)


def test_metric_aliases_do_not_export_marker_as_unauthorized():
    private = {'records': [{'eventual_unauthorized_attempt': True, 'agent_id': 'Dev-C'}]}
    snapshot = deepcopy(private)
    public = marker_names(private)
    assert public == {'records': [{'eventual_marker_attempt': True, 'agent_id': 'Dev-C'}]}
    assert private == snapshot
