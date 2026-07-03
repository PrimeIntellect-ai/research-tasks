# test_final_state.py

import os
import sys
import subprocess
import importlib.util

def test_bad_log_line_file():
    bad_log_path = "/home/user/bad_log_line.txt"
    assert os.path.isfile(bad_log_path), f"File {bad_log_path} does not exist."

    with open(bad_log_path, 'r') as f:
        content = f.read().strip()

    expected_line = '{"status": "error", "timestamp": "2023-10-12T10:00:00Z", "data": corrupted}'
    assert content == expected_line, f"Content of {bad_log_path} is incorrect. Expected: {expected_line}, Got: {content}"

def test_process_logs_patched():
    process_logs_path = "/home/user/process_logs.py"
    assert os.path.isfile(process_logs_path), f"File {process_logs_path} does not exist."

    # Dynamically import the module
    spec = importlib.util.spec_from_file_location("process_logs", process_logs_path)
    process_logs = importlib.util.module_from_spec(spec)

    # We need to set the environment variable so the module loads without crashing
    os.environ['LOG_REGION'] = 'us-east-1'
    try:
        spec.loader.exec_module(process_logs)
    except Exception as e:
        assert False, f"Failed to import process_logs.py: {e}"

    assert hasattr(process_logs, 'process_line'), "process_line function is missing in process_logs.py"
    assert hasattr(process_logs, 'LogFormatError'), "LogFormatError class is missing in process_logs.py"

    # Test the patched function
    bad_line = '{"status": "error", "timestamp": "2023-10-12T10:00:00Z", "data": corrupted}'

    try:
        process_logs.process_line(bad_line)
        assert False, "process_line did not raise an exception for invalid JSON"
    except process_logs.LogFormatError as e:
        assert str(e) == "Invalid log format", f"Expected LogFormatError message to be 'Invalid log format', got '{str(e)}'"
    except Exception as e:
        assert False, f"Expected LogFormatError to be raised, but got {type(e).__name__}: {e}"

def test_regression_test_passes():
    regression_test_path = "/home/user/test_regression.py"
    assert os.path.isfile(regression_test_path), f"File {regression_test_path} does not exist."

    # Run the unittest
    env = os.environ.copy()
    env['LOG_REGION'] = 'us-east-1'
    env['PYTHONPATH'] = '/home/user'

    result = subprocess.run(
        [sys.executable, "-m", "unittest", regression_test_path],
        env=env,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Regression test failed to run or did not pass.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"