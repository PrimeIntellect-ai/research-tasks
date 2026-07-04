# test_final_state.py
import os
import subprocess
import importlib.util
import sys
import pytest

def test_leaked_username_file():
    path = "/home/user/leaked_username.txt"
    assert os.path.isfile(path), f"Expected file {path} to exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "admin_no_semi_4920", f"Expected leaked username to be 'admin_no_semi_4920', got '{content}'"

def test_parser_behavior():
    path = "/home/user/parser.py"
    assert os.path.isfile(path), f"Expected file {path} to exist."

    # Dynamically import the modified parser.py
    spec = importlib.util.spec_from_file_location("parser", path)
    parser = importlib.util.module_from_spec(spec)
    sys.modules["parser"] = parser
    try:
        spec.loader.exec_module(parser)
    except Exception as e:
        pytest.fail(f"Failed to import parser.py: {e}")

    assert hasattr(parser, "process_log"), "parser.py missing process_log function."

    # Test valid line
    try:
        result = parser.process_log("USER_LOGIN: valid_user;")
        assert result is True, "process_log should return True for a valid log line."
    except Exception as e:
        pytest.fail(f"process_log raised an exception for a valid line: {e}")

    # Test invalid line
    with pytest.raises(ValueError) as excinfo:
        parser.process_log("USER_LOGIN: admin_no_semi_4920")

    assert "Missing semicolon" in str(excinfo.value), "ValueError message should be 'Missing semicolon'."

    # Ensure it didn't append to leaked_records
    if hasattr(parser, "leaked_records"):
        assert "admin_no_semi_4920" not in parser.leaked_records, "The username was incorrectly appended to leaked_records."

def test_test_parser_script():
    path = "/home/user/test_parser.py"
    assert os.path.isfile(path), f"Expected file {path} to exist."

    with open(path, "r") as f:
        content = f.read()

    assert "admin_no_semi_4920" in content, "test_parser.py must test the specific leaked username discovered."

    # Run the script
    result = subprocess.run([sys.executable, path], capture_output=True, text=True, cwd="/home/user")
    assert result.returncode == 0, f"test_parser.py failed to run. Output:\n{result.stdout}\n{result.stderr}"