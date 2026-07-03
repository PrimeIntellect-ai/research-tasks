# test_final_state.py

import os
import stat
import subprocess
import csv
import difflib
from datetime import datetime

def test_script_exists_and_executable():
    script_path = "/home/user/run_etl.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_run_script_and_check_csv():
    script_path = "/home/user/run_etl.sh"
    csv_path = "/home/user/correlated_errors.csv"

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    assert os.path.isfile(csv_path), f"Output CSV {csv_path} was not created."

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        lines = list(reader)

    assert len(lines) == 2, f"Expected 2 correlated pairs, but found {len(lines)}."

    # Recompute expected values based on truth logic
    # Pair 1
    msgA1 = "Connection reset by peer"
    msgB1 = "Connection was reset by peer"
    ratio1 = round(difflib.SequenceMatcher(None, msgA1, msgB1).ratio(), 2)

    # Pair 2
    msgA2 = "Database timeout occurred during query"
    msgB2 = "Database timeout during query execution"
    ratio2 = round(difflib.SequenceMatcher(None, msgA2, msgB2).ratio(), 2)

    expected_pair_1 = ["1698240600", "1698240660", f"{ratio1:.2f}", msgA1, msgB1]
    expected_pair_2 = ["1698242400", "1698242520", f"{ratio2:.2f}", msgA2, msgB2]

    # Check that the expected pairs are in the output (order might not be guaranteed, but usually sequential)
    # We will check if both expected pairs exist in the lines

    def match_pair(expected, actual):
        return (
            expected[0] == actual[0] and
            expected[1] == actual[1] and
            abs(float(expected[2]) - float(actual[2])) < 0.02 and
            expected[3] == actual[3] and
            expected[4] == actual[4]
        )

    matched_1 = any(match_pair(expected_pair_1, row) for row in lines)
    matched_2 = any(match_pair(expected_pair_2, row) for row in lines)

    assert matched_1, f"Expected pair 1 not found or incorrect in CSV: {expected_pair_1}"
    assert matched_2, f"Expected pair 2 not found or incorrect in CSV: {expected_pair_2}"

def test_pipeline_log():
    log_path = "/home/user/etl_pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "PIPELINE SUCCESS - Processed 2 correlated pairs" in content, \
        f"Expected success message not found in {log_path}."

def test_cron_job():
    # Check the crontab for user 'user'
    result = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True)
    if result.returncode != 0:
        # Fallback to checking current user if running as user
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)

    assert result.returncode == 0, "Failed to read crontab."

    cron_lines = result.stdout.strip().split('\n')

    # Look for a cron job that runs at the top of the hour
    found_cron = False
    for line in cron_lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 6:
            minute = parts[0]
            command = " ".join(parts[5:])
            if minute == "0" and "/home/user/run_etl.sh" in command:
                found_cron = True
                break

    assert found_cron, "Cron job for /home/user/run_etl.sh at minute 0 not found in crontab."