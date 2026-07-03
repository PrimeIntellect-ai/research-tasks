# test_final_state.py
import os
import json
import stat
import bisect
import pytest

def ks_2samp_manual(data1, data2):
    n1 = len(data1)
    n2 = len(data2)
    data1.sort()
    data2.sort()

    data_all = sorted(data1 + data2)

    max_diff = 0.0
    for val in data_all:
        cdf1 = bisect.bisect_right(data1, val) / n1
        cdf2 = bisect.bisect_right(data2, val) / n2
        diff = abs(cdf1 - cdf2)
        if diff > max_diff:
            max_diff = diff

    return max_diff

def get_expected_results():
    raw_data = []
    with open('/home/user/raw_data.csv', 'r') as f:
        next(f)
        for line in f:
            if line.strip():
                raw_data.append(float(line.strip()))

    ref_data = []
    with open('/home/user/ref_data.csv', 'r') as f:
        next(f)
        for line in f:
            if line.strip():
                ref_data.append(float(line.strip()))

    min_ks = float('inf')
    best_alpha = None
    best_beta = None

    for a in range(21):
        alpha = a * 0.05
        for b in range(21):
            beta = b * 0.10

            y = [alpha * (x ** 2) + beta * x for x in raw_data]
            ks = ks_2samp_manual(y, ref_data)

            if ks < min_ks - 1e-9:
                min_ks = ks
                best_alpha = alpha
                best_beta = beta

    return best_alpha, best_beta, min_ks

def test_run_pipeline_exists_and_executable():
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"Expected script {path} to exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Expected script {path} to be executable."

def test_results_json_exists():
    path = "/home/user/results.json"
    assert os.path.isfile(path), f"Expected results file {path} to exist."

def test_results_json_content():
    path = "/home/user/results.json"
    assert os.path.isfile(path), f"Expected results file {path} to exist."

    with open(path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse {path} as JSON.")

    assert "alpha" in results, "Missing 'alpha' in results.json"
    assert "beta" in results, "Missing 'beta' in results.json"
    assert "ks_stat" in results, "Missing 'ks_stat' in results.json"

    expected_alpha, expected_beta, expected_ks = get_expected_results()

    # Check values with tolerances
    assert abs(results["alpha"] - expected_alpha) < 1e-5, \
        f"Expected alpha ~ {expected_alpha:.2f}, got {results['alpha']}"
    assert abs(results["beta"] - expected_beta) < 1e-5, \
        f"Expected beta ~ {expected_beta:.2f}, got {results['beta']}"
    assert abs(results["ks_stat"] - expected_ks) < 1e-5, \
        f"Expected ks_stat ~ {expected_ks:.6f}, got {results['ks_stat']}"