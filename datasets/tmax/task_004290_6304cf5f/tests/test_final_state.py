# test_final_state.py
import os
import pytest

def test_run_analysis_script_exists_and_executable():
    script_path = "/home/user/run_analysis.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_capacity_summary_contents():
    summary_path = "/home/user/capacity_summary.txt"
    assert os.path.exists(summary_path), f"The summary file {summary_path} does not exist."
    assert os.path.isfile(summary_path), f"The path {summary_path} is not a file."

    # Recompute expected values based on the logic
    # zoneA: fileA1 (12), fileA2 (5), fileA3 (20)
    # zoneB: fileB1 (8), fileB2 (50)
    # Threshold: 10 MB

    zones = ["/home/user/data/zoneA", "/home/user/data/zoneB"]
    total_files = 0
    total_size_mb = 0.0

    for zone in zones:
        if os.path.exists(zone):
            for f in os.listdir(zone):
                fpath = os.path.join(zone, f)
                if os.path.isfile(fpath):
                    size_mb = os.path.getsize(fpath) / (1024 * 1024)
                    if size_mb >= 10.0:
                        total_files += 1
                        total_size_mb += size_mb

    expected_content = f"Total Files: {total_files}\nTotal Size: {total_size_mb:.2f} MB\n"

    with open(summary_path, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), (
        f"Contents of {summary_path} do not match expected results.\n"
        f"Expected:\n{expected_content.strip()}\n"
        f"Actual:\n{actual_content.strip()}"
    )