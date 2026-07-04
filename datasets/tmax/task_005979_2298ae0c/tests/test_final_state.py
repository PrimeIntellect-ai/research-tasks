# test_final_state.py
import os

def test_script_exists_and_executable():
    """Verify that the analyze_locks.sh script exists and is executable."""
    script_path = "/home/user/analyze_locks.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_result_file_exists():
    """Verify that the deadlock_result.txt file exists."""
    result_path = "/home/user/deadlock_result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist."

def test_result_content():
    """Verify that the deadlock result contains the correct transactions."""
    result_path = "/home/user/deadlock_result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist."

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected = "TX_A,TX_B,TX_C,TX_D"
    assert content == expected, f"Expected content '{expected}', but got '{content}'."