# test_final_state.py

import os
import json
import subprocess
import pytest

def get_expected_bad_commit():
    repo_dir = "/home/user/uptime_monitor"
    # The setup script creates the bad commit with a specific message
    result = subprocess.run(
        ["git", "log", "--grep=Update SLA calculation logic to handle edge cases", "--format=%H"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=True
    )
    commit_hash = result.stdout.strip()
    assert commit_hash, "Could not find the expected bad commit in the git history."
    return commit_hash

def test_bad_commit_identified():
    bad_commit_file = "/home/user/bad_commit.txt"
    assert os.path.exists(bad_commit_file), f"{bad_commit_file} does not exist. Did you write the bad commit hash to this file?"

    with open(bad_commit_file, 'r') as f:
        actual_commit = f.read().strip()

    expected_commit = get_expected_bad_commit()
    assert actual_commit == expected_commit, f"The commit hash in {bad_commit_file} is incorrect. Expected {expected_commit}, got {actual_commit}."

def test_sla_report_generated_and_correct():
    report_file = "/home/user/sla_report.json"
    logs_file = "/home/user/data/ping_logs.json"

    assert os.path.exists(report_file), f"The SLA report {report_file} was not generated."
    assert os.path.exists(logs_file), f"The input logs {logs_file} are missing."

    with open(logs_file, 'r') as f:
        logs_data = json.load(f)

    with open(report_file, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The SLA report {report_file} is not valid JSON.")

    for svc, metrics in logs_data.items():
        assert svc in report_data, f"Service '{svc}' is missing from the SLA report."

        total = metrics["total_time_minutes"]
        downtime = metrics["downtime_minutes"]
        expected_sla = (total - downtime) / total * 100.0

        actual_sla = report_data[svc]
        assert abs(actual_sla - expected_sla) < 1e-4, (
            f"Incorrect SLA calculated for {svc}. "
            f"Expected {expected_sla}, got {actual_sla}."
        )

def test_misconfigurations_fixed():
    script_file = "/home/user/uptime_monitor/monitor.py"
    req_file = "/home/user/uptime_monitor/requirements.txt"

    assert os.path.exists(script_file), f"Script {script_file} is missing."
    with open(script_file, 'r') as f:
        script_content = f.read()

    assert "import reqeusts" not in script_content, "The misspelled import 'reqeusts' is still present in monitor.py."

    if os.path.exists(req_file):
        with open(req_file, 'r') as f:
            req_content = f.read()
        assert "reqeusts==" not in req_content, "The misspelled dependency 'reqeusts' is still present in requirements.txt."