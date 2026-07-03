# test_final_state.py

import os
import json
import pytest

def test_build_schedule_exists_and_correct():
    """Verify that the build_schedule.json file is created with the correct execution order and assignments."""
    schedule_file = "/home/user/build_schedule.json"

    assert os.path.exists(schedule_file), f"The file {schedule_file} was not created."
    assert os.path.isfile(schedule_file), f"The path {schedule_file} is not a file."

    try:
        with open(schedule_file, "r") as f:
            schedule = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {schedule_file} does not contain valid JSON.")

    expected_schedule = [
        {"task": "init", "worker": "w-linux-gcc"},
        {"task": "compile_c", "worker": "w-linux-gcc"},
        {"task": "compile_py", "worker": "w-polyglot"},
        {"task": "link", "worker": "w-linux-gcc"},
        {"task": "package", "worker": "w-polyglot"}
    ]

    assert isinstance(schedule, list), "The JSON root must be a list of objects."
    assert len(schedule) == len(expected_schedule), f"Expected {len(expected_schedule)} tasks in schedule, but found {len(schedule)}."

    for i, (actual, expected) in enumerate(zip(schedule, expected_schedule)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."
        assert actual.get("task") == expected["task"], f"Expected task '{expected['task']}' at step {i+1}, got '{actual.get('task')}'."
        assert actual.get("worker") == expected["worker"], f"Expected worker '{expected['worker']}' for task '{expected['task']}' at step {i+1}, got '{actual.get('worker')}'."