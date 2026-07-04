# test_final_state.py

import os
import sys
import math
import pytest
import requests

def test_package_installed():
    try:
        import seq_scorer
    except ImportError:
        pytest.fail("The 'seq_scorer' package is not installed or cannot be imported.")

def get_expected_stats():
    import seq_scorer
    try:
        import h5py
        import numpy as np
    except ImportError:
        pytest.fail("Missing required libraries 'h5py' or 'numpy' to verify expected stats.")

    path = "/app/data/observational.h5"
    assert os.path.isfile(path), f"File {path} does not exist."

    with h5py.File(path, 'r') as f:
        reads = [x.decode('utf-8') if isinstance(x, bytes) else x for x in f['reads'][:]]

    scores = [seq_scorer.score_sequence(seq) for seq in reads]
    mean_score = float(np.mean(scores))

    np.random.seed(42)
    boot_means = []
    n = len(scores)
    # Using numpy for speed and correctness
    for _ in range(10000):
        resample = np.random.choice(scores, size=n, replace=True)
        boot_means.append(np.mean(resample))

    ci_lower = float(np.percentile(boot_means, 2.5))
    ci_upper = float(np.percentile(boot_means, 97.5))

    return mean_score, ci_lower, ci_upper

def test_api_ci_endpoint():
    mean_score, ci_lower, ci_upper = get_expected_stats()

    url = "http://127.0.0.1:8080/ci"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert "mean" in data, "Response missing 'mean' field"
    assert "ci_lower" in data, "Response missing 'ci_lower' field"
    assert "ci_upper" in data, "Response missing 'ci_upper' field"

    assert math.isclose(data["mean"], mean_score, rel_tol=1e-4), f"Expected mean {mean_score}, got {data['mean']}"
    assert math.isclose(data["ci_lower"], ci_lower, rel_tol=1e-4), f"Expected ci_lower {ci_lower}, got {data['ci_lower']}"
    assert math.isclose(data["ci_upper"], ci_upper, rel_tol=1e-4), f"Expected ci_upper {ci_upper}, got {data['ci_upper']}"

def test_api_score_endpoint():
    import seq_scorer
    mean_score, ci_lower, ci_upper = get_expected_stats()

    url = "http://127.0.0.1:8080/score"
    test_sequences = [
        "ATGC",
        "GGCC",
        "AATT",
        "ATGCATGCATGCATGC",
        "GCGCGCGCGCGCGCGC"
    ]

    for seq in test_sequences:
        expected_score = seq_scorer.score_sequence(seq)
        expected_anomalous = expected_score < ci_lower or expected_score > ci_upper

        try:
            response = requests.post(url, json={"sequence": seq}, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to {url}: {e}")

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        data = response.json()
        assert "score" in data, "Response missing 'score' field"
        assert "is_anomalous" in data, "Response missing 'is_anomalous' field"

        assert math.isclose(data["score"], expected_score, rel_tol=1e-4), f"For seq {seq}, expected score {expected_score}, got {data['score']}"
        assert data["is_anomalous"] == expected_anomalous, f"For seq {seq}, expected is_anomalous {expected_anomalous}, got {data['is_anomalous']}"