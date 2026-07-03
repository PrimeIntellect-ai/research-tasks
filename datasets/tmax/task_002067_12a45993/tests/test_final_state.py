# test_final_state.py

import os
import subprocess
import csv

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_configs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_run_script_and_check_outputs():
    script_path = "/home/user/analyze_configs.sh"

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. STDERR:\n{result.stderr}"

    # Check output 1
    stats_path = "/home/user/output/daily_region_stats.csv"
    assert os.path.isfile(stats_path), f"Output file {stats_path} was not created."

    expected_stats = [
        ["date", "region", "daily_total", "rolling_avg"],
        ["2023-11-01", "eu-west", "1", "1.0"],
        ["2023-11-01", "us-east", "3", "3.0"],
        ["2023-11-02", "eu-west", "1", "1.0"],
        ["2023-11-02", "us-east", "3", "3.0"],
        ["2023-11-03", "eu-west", "2", "1.5"],
        ["2023-11-03", "us-east", "1", "2.0"]
    ]

    with open(stats_path, "r") as f:
        reader = csv.reader(f)
        actual_stats = list(reader)

    assert actual_stats == expected_stats, f"Contents of {stats_path} do not match expected.\nExpected: {expected_stats}\nActual: {actual_stats}"

    # Check output 2
    similarity_path = "/home/user/output/host_similarity.csv"
    assert os.path.isfile(similarity_path), f"Output file {similarity_path} was not created."

    expected_similarity = [
        ["db-01", "web-01", "5"],
        ["db-01", "web-02", "4"],
        ["web-01", "web-02", "1"]
    ]

    with open(similarity_path, "r") as f:
        reader = csv.reader(f)
        actual_similarity = list(reader)

    assert actual_similarity == expected_similarity, f"Contents of {similarity_path} do not match expected.\nExpected: {expected_similarity}\nActual: {actual_similarity}"