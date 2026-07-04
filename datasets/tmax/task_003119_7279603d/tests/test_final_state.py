# test_final_state.py

import os
import time
import subprocess
import pytest

def test_fast_log_grep_performance():
    target_executable = "/app/fast-log-grep/build/fast-log-grep"
    test_log = "/app/test_data/massive_log.txt"

    assert os.path.exists(target_executable), f"Executable not found at {target_executable}"
    assert os.path.isfile(target_executable), f"Path {target_executable} is not a file"
    assert os.access(target_executable, os.X_OK), f"Executable {target_executable} is not executable"

    assert os.path.exists(test_log), f"Test log not found at {test_log}"

    start_time = time.time()
    try:
        result = subprocess.run(
            [target_executable, "--query", "ERROR", test_log],
            capture_output=True,
            timeout=10
        )
        end_time = time.time()
    except subprocess.TimeoutExpired:
        pytest.fail("Execution timed out after 10 seconds. Expected execution time <= 0.5 seconds.")

    assert result.returncode == 0, f"Executable failed with return code {result.returncode}.\nStderr: {result.stderr.decode('utf-8', errors='replace')}"

    execution_time = end_time - start_time
    assert execution_time <= 0.5, f"Execution time {execution_time:.3f}s exceeded threshold of 0.5s."