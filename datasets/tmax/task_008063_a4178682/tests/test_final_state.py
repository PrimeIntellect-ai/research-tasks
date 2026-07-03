# test_final_state.py

import os
import csv
import stat

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_report_content():
    csv_path = "/home/user/integrator.csv"
    report_path = "/home/user/report.txt"

    assert os.path.isfile(csv_path), f"Input file {csv_path} is missing."
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    residuals = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            residuals.append(float(row['residual']))

    n = len(residuals)
    assert n > 1, "Not enough data to calculate zero-crossing rate."

    zero_crossings = 0
    for i in range(1, n):
        if residuals[i-1] * residuals[i] < 0:
            zero_crossings += 1

    rate = zero_crossings / (n - 1)

    neg = sum(1 for r in residuals if r < -1.0)
    pos = sum(1 for r in residuals if r > 1.0)
    neu = sum(1 for r in residuals if -1.0 <= r <= 1.0)

    expected_lines = [
        f"Zero-crossing rate: {rate:.4f}",
        f"Negative: {neg}",
        f"Neutral: {neu}",
        f"Positive: {pos}"
    ]
    expected_output = "\n".join(expected_lines)

    with open(report_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Output in {report_path} does not match expected output.\n"
        f"Expected:\n{expected_output}\n\nActual:\n{actual_output}"
    )