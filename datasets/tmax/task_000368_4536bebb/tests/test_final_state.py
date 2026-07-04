# test_final_state.py

import time
import requests
import pytest
import numpy as np
from scipy.stats import ks_2samp, wasserstein_distance

def test_pipeline_end_to_end():
    # Define test data
    test_id = "test_matrix_1"
    matrix = [[1.2, 0.5], [0.5, 1.8]]

    # Compute expected values
    # SVD of the matrix
    U, S, Vh = np.linalg.svd(matrix)

    # Baseline
    baseline = [1.5, 2.1, 0.8, 1.1, 1.9]

    expected_wd = wasserstein_distance(S, baseline)
    ks_stat, ks_pvalue = ks_2samp(S, baseline)
    expected_drift = ks_pvalue < 0.05

    # 1. Post to Ingest API via Nginx
    ingest_url = "http://localhost:8080/ingest"
    payload = {
        "id": test_id,
        "matrix": matrix
    }

    try:
        resp = requests.post(ingest_url, json=payload, timeout=5)
        assert resp.status_code == 200, f"Failed to post to ingest API. Status: {resp.status_code}, Body: {resp.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Could not connect to Nginx ingest endpoint: {e}")

    # 2. Poll the Results API via Nginx
    results_url = "http://localhost:8080/results"

    max_retries = 15
    found = False
    result_data = None

    for _ in range(max_retries):
        try:
            resp = requests.get(results_url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                # The webhook might return a list or a dict containing the results
                # We'll search for our test_id
                if isinstance(data, list):
                    for item in data:
                        if item.get("id") == test_id:
                            found = True
                            result_data = item
                            break
                elif isinstance(data, dict):
                    # Maybe it's a dict keyed by id, or a single object
                    if data.get("id") == test_id:
                        found = True
                        result_data = data
                    elif test_id in data:
                        found = True
                        result_data = data[test_id]

                if found:
                    break
        except requests.exceptions.RequestException:
            pass

        time.sleep(1)

    assert found, f"Did not find result for {test_id} in {results_url} after {max_retries} seconds."

    # 3. Verify the metrics
    assert "wasserstein_distance" in result_data, "Missing wasserstein_distance in result"
    assert "ks_pvalue" in result_data, "Missing ks_pvalue in result"
    assert "drift_detected" in result_data, "Missing drift_detected in result"

    assert np.isclose(result_data["wasserstein_distance"], expected_wd, atol=1e-3), \
        f"Expected wasserstein_distance ~ {expected_wd}, got {result_data['wasserstein_distance']}"

    assert np.isclose(result_data["ks_pvalue"], ks_pvalue, atol=1e-3), \
        f"Expected ks_pvalue ~ {ks_pvalue}, got {result_data['ks_pvalue']}"

    assert result_data["drift_detected"] == expected_drift, \
        f"Expected drift_detected to be {expected_drift}, got {result_data['drift_detected']}"