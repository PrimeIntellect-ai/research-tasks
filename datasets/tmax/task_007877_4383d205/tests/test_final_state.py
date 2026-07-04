# test_final_state.py

import os
import re
import pytest

def test_run_report_script_executable():
    script_path = "/home/user/run_report.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_run_log_exists_and_content():
    log_path = "/home/user/logs/run.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert "REPORT_GENERATED_SUCCESSFULLY" in content, f"Log file {log_path} does not contain 'REPORT_GENERATED_SUCCESSFULLY'."

def test_report_csv_content():
    csv_path = "/home/user/report.csv"
    assert os.path.isfile(csv_path), f"Report file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 4, "CSV file does not contain enough rows (header + 3 teams)."

    header = lines[0]
    assert header == "Team,TotalBytes,Cost,Timestamp", f"Incorrect CSV header: {header}"

    expected_data = {
        "engineering": {"bytes": "15728640", "cost": "0.75"},
        "marketing": {"bytes": "2097152", "cost": "0.10"},
        "sales": {"bytes": "3145728", "cost": "0.15"}
    }

    timestamp_regex = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (EST|EDT)$")

    # Check sorting
    actual_teams = []
    for line in lines[1:]:
        parts = line.split(",")
        assert len(parts) == 4, f"Invalid CSV row format: {line}"
        team, total_bytes, cost, timestamp = parts
        actual_teams.append(team)

        if team in expected_data:
            assert total_bytes == expected_data[team]["bytes"], f"Incorrect bytes for {team}: expected {expected_data[team]['bytes']}, got {total_bytes}"
            assert cost == expected_data[team]["cost"], f"Incorrect cost for {team}: expected {expected_data[team]['cost']}, got {cost}"
            assert timestamp_regex.match(timestamp), f"Invalid timestamp format for {team}: {timestamp}"

    assert actual_teams == sorted(actual_teams), "CSV rows are not sorted alphabetically by Team name."

    for expected_team in expected_data.keys():
        assert expected_team in actual_teams, f"Team {expected_team} missing from CSV."