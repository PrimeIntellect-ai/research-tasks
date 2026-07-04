# test_final_state.py
import os
import re

def test_success_log_exists():
    path = '/home/user/success.log'
    assert os.path.isfile(path), f"The file {path} does not exist. Did you redirect the output?"

def test_success_log_content():
    path = '/home/user/success.log'
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    expected_string = "Processing complete. Final window average: 1.8500"

    assert expected_string in content, (
        f"The success.log does not contain the expected output.\n"
        f"Expected to find: '{expected_string}'\n"
        f"Actual content:\n{content}"
    )

def test_stat_service_fixed():
    path = '/home/user/stat_service.py'
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    # Check that the memory leak (unbounded growth of all_history) was addressed
    # We can check if all_history is still appended to without bounds, or if the MemoryError was removed.
    # But since the user might fix it in various ways, the success.log is the ultimate proof.
    # However, we can check if the script runs without errors.
    import subprocess
    result = subprocess.run(['python3', path], capture_output=True, text=True)
    assert result.returncode == 0, (
        f"The script {path} still fails when executed.\n"
        f"Error output:\n{result.stderr}"
    )

    # Check that the output matches the expected output
    expected_string = "Processing complete. Final window average: 1.8500"
    assert expected_string in result.stdout, (
        f"The script output does not match the expected final average.\n"
        f"Expected to find: '{expected_string}'\n"
        f"Actual output:\n{result.stdout}"
    )