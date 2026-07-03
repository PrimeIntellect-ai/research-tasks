# test_final_state.py
import os
import sys
import pytest
import requests
import numpy as np

def test_server_script_exists():
    assert os.path.isfile('/home/user/server.py'), "/home/user/server.py is missing"

def test_seqtools_fixed():
    sys.path.insert(0, '/app')
    try:
        from seqtools.scorer import WEIGHT_MATRIX, score_profile
    except ImportError as e:
        pytest.fail(f"Failed to import seqtools: {e}")

    assert WEIGHT_MATRIX.shape == (4, 4), f"WEIGHT_MATRIX should be 4x4, but is {WEIGHT_MATRIX.shape}"
    assert np.array_equal(WEIGHT_MATRIX, np.eye(4)), "WEIGHT_MATRIX is not a 4x4 identity matrix"

    # Test that score_profile works without ValueError
    try:
        scores = score_profile("ACGT")
        assert len(scores) == 4
    except Exception as e:
        pytest.fail(f"score_profile failed: {e}")

def test_analyze_endpoint():
    # Test with a uniform sequence (all valid bases, sum = 1.0)
    seq1 = "ACGTACGTACGT"
    payload1 = {"sequence": seq1}

    try:
        resp1 = requests.post("http://127.0.0.1:8080/analyze", json=payload1, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at 127.0.0.1:8080: {e}")

    assert resp1.status_code == 200, f"Expected status code 200, got {resp1.status_code}"
    data1 = resp1.json()
    assert "derivative" in data1, "Response JSON missing 'derivative' key"

    # For a sequence of all valid bases, the scores are all 1.0, so the gradient is all 0.0
    expected_derivative1 = [0.0] * len(seq1)
    np.testing.assert_allclose(
        data1["derivative"], 
        expected_derivative1, 
        err_msg="Derivative for 'ACGTACGTACGT' is incorrect"
    )

    # Test with a sequence containing an invalid base (sum = 0.0 for 'X')
    seq2 = "ACXGT"
    payload2 = {"sequence": seq2}
    resp2 = requests.post("http://127.0.0.1:8080/analyze", json=payload2, timeout=2)
    assert resp2.status_code == 200
    data2 = resp2.json()

    # Scores: A=1, C=1, X=0, G=1, T=1
    # Gradient of [1, 1, 0, 1, 1]:
    # index 0: 1 - 1 = 0
    # index 1: (0 - 1) / 2 = -0.5
    # index 2: (1 - 1) / 2 = 0.0
    # index 3: (1 - 0) / 2 = 0.5
    # index 4: 1 - 1 = 0
    expected_derivative2 = [0.0, -0.5, 0.0, 0.5, 0.0]
    np.testing.assert_allclose(
        data2["derivative"], 
        expected_derivative2, 
        err_msg="Derivative for 'ACXGT' is incorrect"
    )