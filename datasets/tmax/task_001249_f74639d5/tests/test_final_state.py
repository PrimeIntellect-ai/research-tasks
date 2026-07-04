# test_final_state.py

import os
import pytest

def test_fixed_audit_report_exists():
    report_path = "/home/user/fixed_audit_report.csv"
    assert os.path.isfile(report_path), f"The expected output file {report_path} does not exist."

def test_fixed_audit_report_contents():
    report_path = "/home/user/fixed_audit_report.csv"
    assert os.path.isfile(report_path), f"The expected output file {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Alice,CI-CD",
        "Alice,Prod-DB",
        "Alice,Wiki",
        "Bob,CI-CD",
        "Bob,Wiki",
        "Charlie,Wiki"
    ]

    assert lines == expected_lines, (
        f"The contents of {report_path} do not match the expected correct output.\n"
        f"Expected:\n{expected_lines}\n"
        f"Got:\n{lines}"
    )

def test_generate_audit_script_modified():
    script_path = "/home/user/generate_audit.sh"
    assert os.path.isfile(script_path), f"The script file {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    # The original flawed script had an implicit cross join without proper WHERE clauses.
    # We check that the flawed WHERE clause is no longer exactly the same, or that JOINs are used.
    original_flawed_where = "WHERE u.id = ur.user_id;"
    original_flawed_from = "FROM users u, systems s, user_roles ur, role_systems rs"

    # It's possible the user just ran sqlite3 directly, but the instructions say:
    # "Fix the SQL query inside the bash script /home/user/generate_audit.sh"
    # So we should verify the script was changed.
    is_fixed = (original_flawed_from not in content) or (original_flawed_where not in content) or ("JOIN" in content.upper())
    assert is_fixed, "The script /home/user/generate_audit.sh still appears to contain the original flawed cross join query."