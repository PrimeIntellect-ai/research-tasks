# test_final_state.py
import os
import subprocess
import pytest

def test_script_exists():
    script_path = "/home/user/compare_models.sh"
    assert os.path.isfile(script_path), f"Bash script not found at expected absolute path: {script_path}"

def test_report_exists():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Deliverable report not found at expected absolute path: {report_path}"

def test_report_content():
    report_path = "/home/user/report.txt"
    with open(report_path, "r") as f:
        actual_report = f.read().strip()

    # We use a subprocess to compute the expected output using numpy, 
    # since we are restricted to the Python standard library in this pytest file,
    # but the environment has numpy installed and we must match its specific random state.
    canonical_logic = """
import numpy as np

np.random.seed(123)
ref_data = np.random.normal(loc=50.0, scale=5.0, size=500)
test_data = np.random.normal(loc=48.0, scale=4.5, size=500)

ref_mean = np.mean(ref_data)
ref_std = np.std(ref_data, ddof=1)
test_mean = np.mean(test_data)
test_std = np.std(test_data, ddof=1)

np.random.seed(42)
diffs = []
for _ in range(5000):
    b_test = np.random.choice(test_data, size=len(test_data), replace=True)
    b_ref = np.random.choice(ref_data, size=len(ref_data), replace=True)
    diffs.append(np.mean(b_test) - np.mean(b_ref))

ci_lower = np.percentile(diffs, 2.5)
ci_upper = np.percentile(diffs, 97.5)

expected_report = f"Ref: Mean={ref_mean:.2f}, Std={ref_std:.2f}\\n"
expected_report += f"Test: Mean={test_mean:.2f}, Std={test_std:.2f}\\n"
expected_report += f"CI: [{ci_lower:.2f}, {ci_upper:.2f}]\\n"
expected_report += "Conclusion: IMPROVED"
print(expected_report)
"""

    result = subprocess.run(
        ['python3', '-c', canonical_logic], 
        capture_output=True, 
        text=True, 
        check=True
    )
    expected_report = result.stdout.strip()

    assert actual_report == expected_report, (
        f"The content of {report_path} does not match the expected output.\n"
        f"--- Expected ---\n{expected_report}\n"
        f"--- Got ---\n{actual_report}"
    )