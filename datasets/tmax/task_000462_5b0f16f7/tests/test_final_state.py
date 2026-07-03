# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/organizer.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_build_order_log():
    log_path = "/home/user/build_order.log"
    assert os.path.isfile(log_path), f"Build order log {log_path} does not exist."

    expected_order = [
        "common.proto",
        "db.proto",
        "user.proto",
        "auth.proto",
        "gateway.proto"
    ]

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_order, f"Expected build order {expected_order}, but got {lines}."

def test_compiled_protos_directory():
    target_dir = "/home/user/compiled_protos"
    assert os.path.isdir(target_dir), f"Target directory {target_dir} does not exist."

    expected_files = {
        "common.proto": 1,
        "db.proto": 2,
        "user.proto": 3,
        "auth.proto": 4,
        "gateway.proto": 5
    }

    for filename, order in expected_files.items():
        filepath = os.path.join(target_dir, filename)
        assert os.path.isfile(filepath), f"Compiled proto file {filepath} is missing."

        with open(filepath, 'r') as f:
            first_line = f.readline().strip()

        expected_line = f"// ORDER: {order}"
        assert first_line == expected_line, f"Expected {filepath} to start with '{expected_line}', but got '{first_line}'."