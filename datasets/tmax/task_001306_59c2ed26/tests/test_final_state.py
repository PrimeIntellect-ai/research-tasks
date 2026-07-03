# test_final_state.py

import os
import subprocess
import pytest

def get_golden_data():
    golden_lines = []
    for seed in [1, 2, 3, 4]:
        out = subprocess.check_output(["/home/user/generate_data.sh", str(seed)], text=True)
        # Filter out empty lines
        lines = [line for line in out.split('\n') if line.strip()]
        golden_lines.extend(lines)
    return golden_lines

@pytest.fixture(scope="session")
def golden_stats():
    lines = get_golden_data()

    sum1 = 0.0
    sum2 = 0.0
    b1 = b2 = b3 = b4 = b5 = 0
    count = 0

    for line in lines:
        cols = line.split(',')
        if len(cols) < 10:
            continue

        sum1 += float(cols[0])
        sum2 += float(cols[1])
        count += 1

        v = float(cols[2])
        if 0 <= v < 20:
            b1 += 1
        elif 20 <= v < 40:
            b2 += 1
        elif 40 <= v < 60:
            b3 += 1
        elif 60 <= v < 80:
            b4 += 1
        elif 80 <= v <= 100:
            b5 += 1

    diff_val = (sum2 / count) - (sum1 / count) if count > 0 else 0.0
    diff_str = f"{diff_val:.3f}"
    hist_str = f"{b1}\n{b2}\n{b3}\n{b4}\n{b5}"

    return {
        "lines": lines,
        "diff": diff_str,
        "hist": hist_str
    }

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_combined_csv(golden_stats):
    combined_path = "/home/user/combined.csv"
    assert os.path.exists(combined_path), f"The file {combined_path} does not exist."

    with open(combined_path, "r") as f:
        content = f.read().strip().split('\n')

    actual_lines = [line for line in content if line.strip()]
    expected_lines = golden_stats["lines"]

    assert len(actual_lines) == 4000, f"Expected 4000 lines in combined.csv, found {len(actual_lines)}."

    # Check first and last few lines to ensure correct concatenation order
    assert actual_lines[:5] == expected_lines[:5], "The beginning of combined.csv does not match the expected output for seed 1."
    assert actual_lines[-5:] == expected_lines[-5:], "The end of combined.csv does not match the expected output for seed 4."

def test_diff_txt(golden_stats):
    diff_path = "/home/user/diff.txt"
    assert os.path.exists(diff_path), f"The file {diff_path} does not exist."

    with open(diff_path, "r") as f:
        actual_diff = f.read().strip()

    expected_diff = golden_stats["diff"]
    assert actual_diff == expected_diff, f"Expected difference {expected_diff}, but found {actual_diff} in diff.txt."

def test_hist_txt(golden_stats):
    hist_path = "/home/user/hist.txt"
    assert os.path.exists(hist_path), f"The file {hist_path} does not exist."

    with open(hist_path, "r") as f:
        actual_hist = f.read().strip()

    expected_hist = golden_stats["hist"]
    assert actual_hist == expected_hist, f"Expected histogram counts:\n{expected_hist}\nBut found:\n{actual_hist}"