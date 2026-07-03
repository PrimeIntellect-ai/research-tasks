# test_final_state.py

import os
import pytest

def test_restore_plan_log_exists():
    path = "/home/user/restore_plan.log"
    assert os.path.isfile(path), f"The file {path} was not created."

def test_restore_plan_log_content():
    path = "/home/user/restore_plan.log"
    assert os.path.isfile(path), f"The file {path} was not created."

    expected_lines = [
        "3: analytics_db",
        "3: notification_db",
        "2: billing_db",
        "2: profile_db",
        "2: recommendation_db",
        "1: user_db"
    ]

    with open(path, "r") as f:
        # Read lines, strip whitespace, and ignore empty lines
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )