# test_final_state.py

import os
import subprocess
import re
import pytest

def get_expected_values():
    repo_dir = "/home/user/log_engine"

    # Get all commits in chronological order
    result = subprocess.run(
        ["git", "log", "--reverse", "--format=%H"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=True
    )
    commits = result.stdout.strip().splitlines()

    bad_commit = None
    segfault_line = None

    for commit in commits:
        # Show processor.c at this commit
        res = subprocess.run(
            ["git", "show", f"{commit}:processor.c"],
            cwd=repo_dir,
            capture_output=True,
            text=True
        )
        if res.returncode != 0:
            continue
        content = res.stdout
        if "strtok" in content and "atoi(token)" in content:
            bad_commit = commit
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if "int duration = atoi(token);" in line:
                    segfault_line = i + 1
                    break
            break

    return bad_commit, "process_line", segfault_line, 432

def test_diagnostic_report_exists():
    report_file = "/home/user/diagnostic_report.txt"
    assert os.path.isfile(report_file), f"Diagnostic report {report_file} does not exist."

def test_diagnostic_report_content():
    report_file = "/home/user/diagnostic_report.txt"
    assert os.path.isfile(report_file), f"Diagnostic report {report_file} does not exist."

    expected_bad_commit, expected_segfault_func, expected_segfault_line, expected_anomalous_line = get_expected_values()

    assert expected_bad_commit is not None, "Could not determine the bad commit from the repository history."
    assert expected_segfault_line is not None, "Could not determine the segfault line from the bad commit."

    with open(report_file, 'r') as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 lines in the diagnostic report, but found {len(lines)}."

    parsed_data = {}
    for line in lines:
        if ":" in line:
            key, val = line.split(":", 1)
            parsed_data[key.strip()] = val.strip()

    assert "Bad Commit" in parsed_data, "Missing 'Bad Commit' in the report."
    assert parsed_data["Bad Commit"] == expected_bad_commit, f"Incorrect Bad Commit. Expected {expected_bad_commit}, got {parsed_data['Bad Commit']}"

    assert "Segfault Function" in parsed_data, "Missing 'Segfault Function' in the report."
    assert parsed_data["Segfault Function"] == expected_segfault_func, f"Incorrect Segfault Function. Expected {expected_segfault_func}, got {parsed_data['Segfault Function']}"

    assert "Segfault Line" in parsed_data, "Missing 'Segfault Line' in the report."
    assert parsed_data["Segfault Line"] == str(expected_segfault_line), f"Incorrect Segfault Line. Expected {expected_segfault_line}, got {parsed_data['Segfault Line']}"

    assert "Anomalous Data Line" in parsed_data, "Missing 'Anomalous Data Line' in the report."
    assert parsed_data["Anomalous Data Line"] == str(expected_anomalous_line), f"Incorrect Anomalous Data Line. Expected {expected_anomalous_line}, got {parsed_data['Anomalous Data Line']}"