# test_final_state.py

import os
import json
import numpy as np
import scipy.stats as stats
import pytest

def test_fastvecsearch_installed_and_fixed():
    try:
        import fastvecsearch
    except ImportError:
        pytest.fail("fastvecsearch package is not installed or importable.")

    assert hasattr(fastvecsearch, 'cosine_sim'), "fastvecsearch is missing 'cosine_sim'"

    try:
        # Test the fixed code
        res = fastvecsearch.cosine_sim(np.array([1, 0]), np.array([0, 1]))
        assert np.isclose(res, 0.0), "cosine_sim did not return expected result"
    except Exception as e:
        pytest.fail(f"fastvecsearch.cosine_sim failed or is still broken: {e}")

def test_hard_negatives_json_metrics():
    json_path = '/home/user/hard_negatives.json'
    assert os.path.exists(json_path), f"Output file missing: {json_path}"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "hard_negative_indices" in data, "Missing 'hard_negative_indices' in JSON"
    assert "ttest_p_value" in data, "Missing 'ttest_p_value' in JSON"
    assert "ci_lower" in data, "Missing 'ci_lower' in JSON"
    assert "ci_upper" in data, "Missing 'ci_upper' in JSON"

    agent_indices = np.array(data["hard_negative_indices"])
    assert agent_indices.shape == (500, 5), f"Expected 'hard_negative_indices' shape (500, 5), got {agent_indices.shape}"

    anchors_path = '/home/user/data/anchors.npy'
    candidates_path = '/home/user/data/candidates.npy'
    assert os.path.exists(anchors_path), f"Missing {anchors_path}"
    assert os.path.exists(candidates_path), f"Missing {candidates_path}"

    anchors = np.load(anchors_path)
    candidates = np.load(candidates_path)

    # Compute ground truth indices
    sims = anchors @ candidates.T
    gt_indices = np.argsort(-sims, axis=1)[:, :5]

    # Calculate overlap metric
    overlaps = []
    for i in range(500):
        overlaps.append(len(set(agent_indices[i]) & set(gt_indices[i])) / 5.0)
    mean_overlap = np.mean(overlaps)

    assert mean_overlap >= 0.98, f"Mean overlap too low. Expected >= 0.98, got {mean_overlap}"

    # Calculate ground truth stats
    np.random.seed(42)
    gt_hard_means = np.mean(np.take_along_axis(sims, gt_indices, axis=1), axis=1)
    random_indices = np.random.choice(candidates.shape[0], size=(500, 5))
    gt_rand_means = np.mean(np.take_along_axis(sims, random_indices, axis=1), axis=1)

    res = stats.ttest_rel(gt_hard_means, gt_rand_means)
    ci = res.confidence_interval(confidence_level=0.95)

    # Check metrics
    p_val_err = abs(data['ttest_p_value'] - res.pvalue)
    assert p_val_err <= 1e-4, f"p-value absolute error > 1e-4. Expected ~{res.pvalue}, got {data['ttest_p_value']} (err: {p_val_err})"

    ci_low_err = abs(data['ci_lower'] - ci.low)
    assert ci_low_err <= 1e-4, f"ci_lower absolute error > 1e-4. Expected ~{ci.low}, got {data['ci_lower']} (err: {ci_low_err})"

    ci_high_err = abs(data['ci_upper'] - ci.high)
    assert ci_high_err <= 1e-4, f"ci_upper absolute error > 1e-4. Expected ~{ci.high}, got {data['ci_upper']} (err: {ci_high_err})"