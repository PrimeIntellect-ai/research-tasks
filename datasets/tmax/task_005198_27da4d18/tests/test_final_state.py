# test_final_state.py
import os
import pytest

def test_threat_count_accuracy():
    """
    Check that the numerical count in /home/user/threat_count.txt
    is within the acceptable threshold (<= 5) of the ground truth (42).
    """
    count_file = '/home/user/threat_count.txt'
    assert os.path.exists(count_file), f"File {count_file} does not exist."

    with open(count_file, 'r') as f:
        content = f.read().strip()

    try:
        agent_val = int(content)
    except ValueError:
        pytest.fail(f"Content of {count_file} is not a valid integer: '{content}'")

    truth_val = 42
    diff = abs(agent_val - truth_val)

    assert diff <= 5, f"Expected count close to {truth_val}, but got {agent_val}. Difference {diff} exceeds threshold of 5."

def test_analyze_logs_script_exists():
    """
    Check that the script /home/user/analyze_logs.sh exists.
    """
    script_file = '/home/user/analyze_logs.sh'
    assert os.path.exists(script_file), f"Script {script_file} does not exist."
    assert os.path.isfile(script_file), f"{script_file} is not a regular file."