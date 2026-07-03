# test_final_state.py
import os
import re
import pytest

def test_dnastat_directory_exists():
    assert os.path.isdir("/home/user/dnastat"), "Directory /home/user/dnastat does not exist."

def test_analyzer_go_exists():
    assert os.path.isfile("/home/user/dnastat/analyzer.go"), "File /home/user/dnastat/analyzer.go does not exist."

def test_run_analysis_sh_exists():
    assert os.path.isfile("/home/user/dnastat/run_analysis.sh"), "File /home/user/dnastat/run_analysis.sh does not exist."

def test_results_log_exists():
    assert os.path.isfile("/home/user/dnastat/results.log"), "File /home/user/dnastat/results.log does not exist. Did you run the bash script?"

def test_results_log_content():
    log_path = "/home/user/dnastat/results.log"
    if not os.path.isfile(log_path):
        pytest.fail(f"File {log_path} not found.")

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines of output in results.log, found {len(lines)}."

    # Check seq1.txt output
    seq1_match = re.search(r"File:\s*seq1\.txt,\s*Z:\s*([0-9.]+),\s*Hypothesis:\s*Random", lines[0])
    assert seq1_match is not None, f"Line 1 does not match expected format for seq1.txt. Got: {lines[0]}"
    z1 = float(seq1_match.group(1))
    assert 1.5 < z1 < 1.7, f"Z-score for seq1.txt is out of expected range (expected ~1.63). Got: {z1}"

    # Check seq2.txt output
    seq2_match = re.search(r"File:\s*seq2\.txt,\s*Z:\s*([0-9.]+),\s*Hypothesis:\s*Periodic", lines[1])
    assert seq2_match is not None, f"Line 2 does not match expected format for seq2.txt. Got: {lines[1]}"
    z2 = float(seq2_match.group(1))
    assert 3.2 < z2 < 3.4, f"Z-score for seq2.txt is out of expected range (expected ~3.33). Got: {z2}"