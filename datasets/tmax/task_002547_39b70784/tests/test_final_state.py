# test_final_state.py
import os
import csv
import re
import subprocess
import pytest

def test_video_data_long_csv():
    csv_path = "/home/user/video_data_long.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["second_offset", "sensor_name", "state"], f"Incorrect CSV header: {header}"

        rows = list(reader)

    assert len(rows) == 15, f"Expected 15 rows in CSV, found {len(rows)}"

    # Expected truth values based on the video fixture
    expected_states = {
        0: {"red": 1, "green": 0, "blue": 0},
        1: {"red": 1, "green": 1, "blue": 0},
        2: {"red": 0, "green": 1, "blue": 1},
        3: {"red": 0, "green": 0, "blue": 1},
        4: {"red": 1, "green": 1, "blue": 1},
    }

    parsed_rows = []
    for row in rows:
        assert len(row) == 3, f"Invalid row length: {row}"
        offset = int(row[0])
        sensor = row[1]
        state = int(row[2])
        parsed_rows.append((offset, sensor, state))

    # Check sorting
    sorted_rows = sorted(parsed_rows, key=lambda x: (x[0], x[1]))
    assert parsed_rows == sorted_rows, "CSV rows are not sorted by second_offset then sensor_name."

    for offset, sensor, state in parsed_rows:
        assert expected_states[offset][sensor] == state, f"Incorrect state for second {offset}, sensor {sensor}: expected {expected_states[offset][sensor]}, got {state}"

def test_validator_script():
    script_path = "/home/user/validator.py"
    assert os.path.isfile(script_path), f"Validator script {script_path} does not exist."

    # Test Clean Corpus
    clean_dir = "/app/corpus/clean/"
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".json")]

    result_clean = subprocess.run(["python3", script_path, clean_dir], capture_output=True, text=True)
    assert result_clean.returncode == 0, f"Validator script failed on clean corpus with error: {result_clean.stderr}"

    clean_output = result_clean.stdout.strip().split("\n")
    clean_output = [line.strip() for line in clean_output if line.strip()]

    rejected_clean = []
    for f in clean_files:
        expected_line = f"ACCEPT: {f}"
        if expected_line not in clean_output:
            rejected_clean.append(f)

    # Test Evil Corpus
    evil_dir = "/app/corpus/evil/"
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".json")]

    result_evil = subprocess.run(["python3", script_path, evil_dir], capture_output=True, text=True)
    assert result_evil.returncode == 0, f"Validator script failed on evil corpus with error: {result_evil.stderr}"

    evil_output = result_evil.stdout.strip().split("\n")
    evil_output = [line.strip() for line in evil_output if line.strip()]

    accepted_evil = []
    for f in evil_files:
        expected_line = f"REJECT: {f}"
        if expected_line not in evil_output:
            accepted_evil.append(f)

    error_msgs = []
    if rejected_clean:
        error_msgs.append(f"{len(rejected_clean)} of {len(clean_files)} clean files modified/rejected: {', '.join(rejected_clean)}")
    if accepted_evil:
        error_msgs.append(f"{len(accepted_evil)} of {len(evil_files)} evil files bypassed/accepted: {', '.join(accepted_evil)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_report_txt():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = """FACTORY ETL REPORT
Total seconds recorded: 5
Red sensor ON duration: 3 seconds
Green sensor ON duration: 3 seconds
Blue sensor ON duration: 3 seconds"""

    assert content == expected_content, f"Report content mismatch.\nExpected:\n{expected_content}\n\nGot:\n{content}"