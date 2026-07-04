# test_final_state.py

import os
import pytest

def test_restore_plan_correct():
    target_file = "/home/user/restore_plan.txt"

    assert os.path.exists(target_file), f"The file {target_file} does not exist."
    assert os.path.isfile(target_file), f"{target_file} is not a file."

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_content = "Total Time: 35 mins\nPath: DB_MAIN_FULL -> INC_1 -> INC_3 -> RESTORE_COMPLETE"

    # Normalize line endings and whitespace for robustness
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = expected_content.splitlines()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output, found {len(actual_lines)}."

    assert actual_lines[0] == expected_lines[0], f"First line mismatch. Expected '{expected_lines[0]}', got '{actual_lines[0]}'."
    assert actual_lines[1] == expected_lines[1], f"Second line mismatch. Expected '{expected_lines[1]}', got '{actual_lines[1]}'."