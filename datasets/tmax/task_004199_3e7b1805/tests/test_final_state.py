# test_final_state.py
import os
import pytest

def test_analyze_kmers_script_exists():
    assert os.path.isfile('/home/user/analyze_kmers.py'), "/home/user/analyze_kmers.py script does not exist."

def test_svd_out_file():
    svd_file = '/home/user/svd_out.txt'
    assert os.path.isfile(svd_file), f"{svd_file} does not exist."

    with open(svd_file, 'r') as f:
        content = f.read().strip()

    assert content != "", f"{svd_file} is empty."

    # Expected values derived from the truth data
    expected_values = [35.3115, 10.0354, 8.1209]

    try:
        actual_values = [float(x.strip()) for x in content.split(',')]
    except ValueError:
        pytest.fail(f"Could not parse comma-separated floats from {svd_file}. Content: {content}")

    assert len(actual_values) == 3, f"Expected 3 singular values, got {len(actual_values)}."

    for actual, expected in zip(actual_values, expected_values):
        assert abs(actual - expected) <= 1e-3, f"Singular value {actual} differs from expected {expected}."

def test_w_sum_file():
    w_sum_file = '/home/user/w_sum.txt'
    assert os.path.isfile(w_sum_file), f"{w_sum_file} does not exist."

    with open(w_sum_file, 'r') as f:
        content = f.read().strip()

    assert content != "", f"{w_sum_file} is empty."

    expected_w_sum = 0.2606

    try:
        actual_w_sum = float(content)
    except ValueError:
        pytest.fail(f"Could not parse float from {w_sum_file}. Content: {content}")

    assert abs(actual_w_sum - expected_w_sum) <= 1e-3, f"w_sum {actual_w_sum} differs from expected {expected_w_sum}."