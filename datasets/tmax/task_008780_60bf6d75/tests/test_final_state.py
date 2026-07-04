# test_final_state.py
import os

def test_find_damping_script_exists():
    """Check if the find_damping.py script was created."""
    script_path = '/home/user/find_damping.py'
    assert os.path.isfile(script_path), f"The script {script_path} is missing. You must create it."

def test_best_c_log_exists_and_correct():
    """Check if best_c.log exists and contains the correct value."""
    log_path = '/home/user/best_c.log'
    assert os.path.isfile(log_path), f"The log file {log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_content = "BEST_C=0.5"
    assert content == expected_content, f"The file {log_path} contains '{content}', but expected '{expected_content}'."