# test_final_state.py

import os
import subprocess

def test_minimal_fail_txt():
    """Check if minimal_fail.txt contains the exact failing line."""
    path = "/home/user/minimal_fail.txt"
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    expected_line = "2023-10-15T12:00:00Z\n"
    assert content == expected_line, f"Expected {path} to contain exactly '{expected_line}', but got '{content}'."

def test_profiler_script_fixes():
    """Check if profiler.py can process the log file without hanging and produces the correct result."""
    script_path = "/home/user/profiler.py"
    log_path = "/home/user/app_logs.txt"
    result_path = "/home/user/result.txt"

    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.path.isfile(log_path), f"{log_path} is missing."

    # Remove result.txt if it exists to ensure the script generates it
    if os.path.exists(result_path):
        os.remove(result_path)

    try:
        # Run the script with a timeout to detect infinite loops
        subprocess.run(
            ["python3", script_path, log_path],
            check=True,
            timeout=5,
            capture_output=True,
            text=True
        )
    except subprocess.TimeoutExpired:
        assert False, "The script profiler.py timed out. It seems the infinite loop is not fixed."
    except subprocess.CalledProcessError as e:
        assert False, f"The script profiler.py crashed with error: {e.stderr}"

    assert os.path.isfile(result_path), f"The script did not generate {result_path}."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected_content = "Processed: 1101, Total Offset: 114000"
    assert content == expected_content, f"Expected result.txt to contain '{expected_content}', but got '{content}'."