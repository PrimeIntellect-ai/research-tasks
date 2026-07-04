# test_final_state.py
import os
import json
import csv
import math

def test_report_json_exists():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

def test_report_json_contents():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} is not valid JSON."

    expected_keys = {"dominant_frequency", "wasserstein_distance", "bootstrap_ci_lower", "bootstrap_ci_upper"}
    assert set(report.keys()) == expected_keys, f"JSON keys do not match expected. Got {list(report.keys())}"

    # 1. Check Dominant Frequency
    assert math.isclose(report["dominant_frequency"], 8.00, abs_tol=0.01), \
        f"Expected dominant_frequency to be 8.00, got {report['dominant_frequency']}"

    # 2. Recompute Wasserstein distance from CSV
    csv_path = "/home/user/sim_data.csv"
    stable_err = []
    unstable_err = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stable_err.append(float(row['stable_err']))
            unstable_err.append(float(row['unstable_err']))

    stable_err.sort()
    unstable_err.sort()

    wasserstein = sum(abs(s - u) for s, u in zip(stable_err, unstable_err)) / len(stable_err)

    assert math.isclose(report["wasserstein_distance"], wasserstein, abs_tol=0.05), \
        f"Expected wasserstein_distance around {wasserstein:.2f}, got {report['wasserstein_distance']}"

    # 3. Check Bootstrap CI bounds
    # The actual values depend on Go's math/rand with seed 42. 
    # The true mean of unstable_err is around 0.05. 
    # CI lower is ~0.01, CI upper is ~0.09.
    assert math.isclose(report["bootstrap_ci_lower"], 0.01, abs_tol=0.05), \
        f"Expected bootstrap_ci_lower around 0.01, got {report['bootstrap_ci_lower']}"
    assert math.isclose(report["bootstrap_ci_upper"], 0.09, abs_tol=0.05), \
        f"Expected bootstrap_ci_upper around 0.09, got {report['bootstrap_ci_upper']}"