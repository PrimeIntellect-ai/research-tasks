# test_final_state.py
import os
import subprocess
import pytest

def test_august_report_content():
    report_path = "/home/user/legacy_analytics/august_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip().splitlines()

    # Expected output:
    expected = [
        "user_1: 2500",
        "user_2: 2000",
        "user_3: 800"
    ]

    assert sorted(content) == sorted(expected), f"Content of {report_path} is incorrect. Expected {expected}, got {content}"

def test_mre_csv_content():
    mre_path = "/home/user/legacy_analytics/mre.csv"
    assert os.path.isfile(mre_path), f"MRE file {mre_path} is missing."

    with open(mre_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 2, f"MRE file should have exactly 2 lines (header + 1 data row), but has {len(lines)}."

    header = lines[0]
    data_row = lines[1]

    # Check if data row has 08 or 09 in the month part
    parts = data_row.split(",")
    assert len(parts) >= 3, "Data row in MRE file does not have enough columns."

    date_part = parts[0]
    date_split = date_part.split("-")
    assert len(date_split) >= 2, "Date format in MRE file is incorrect."

    month = date_split[1]
    assert month in ["08", "09"], f"The month in the MRE data row should be '08' or '09' to trigger the octal bug, got '{month}'."

def test_process_logs_script_fixed():
    script_path = "/home/user/legacy_analytics/process_logs.sh"
    csv_path = "/home/user/legacy_analytics/access_logs.csv"

    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Run the script and check output
    result = subprocess.run([script_path, csv_path, "8"], capture_output=True, text=True)

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    output_lines = result.stdout.strip().splitlines()
    expected = [
        "user_1: 2500",
        "user_2: 2000",
        "user_3: 800"
    ]

    assert sorted(output_lines) == sorted(expected), f"Script output is incorrect. Expected {expected}, got {output_lines}"