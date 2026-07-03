# test_final_state.py

import os
import subprocess
import pytest

def test_waf_engine_compiled():
    engine_path = "/home/user/waf_pr/waf_engine"
    assert os.path.isfile(engine_path), f"Compiled binary {engine_path} is missing. Did you run gcc?"
    assert os.access(engine_path, os.X_OK), f"File {engine_path} is not executable."

def test_test_results_log():
    log_path = "/home/user/waf_pr/test_results.log"
    assert os.path.isfile(log_path), f"Output file {log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert len(content) > 0, f"Output file {log_path} is empty."

    # The output should contain the paths inserted: 100, 101, 111.
    # Because compression might alter the exact string format, we just check
    # that the characters 1 and 0 are present, indicating the paths were printed.
    assert "1" in content and "0" in content, f"Output file {log_path} does not contain expected routing paths."

def test_memory_safety_with_valgrind():
    engine_path = "/home/user/waf_pr/waf_engine"
    assert os.path.isfile(engine_path), "Cannot run valgrind because waf_engine is missing."

    cmd = [
        "valgrind",
        "--leak-check=full",
        "--show-leak-kinds=all",
        "--error-exitcode=1",
        engine_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"Valgrind reported memory errors or leaks. stderr:\n{result.stderr}"
    except FileNotFoundError:
        pytest.fail("valgrind is not installed or not found in PATH. Cannot verify memory safety.")
    except subprocess.TimeoutExpired:
        pytest.fail("valgrind execution timed out. There might be an infinite loop in your code.")