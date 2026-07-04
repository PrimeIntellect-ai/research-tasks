# test_final_state.py
import os

def test_rotated_password_log_exists():
    """Verify that the rotated_password.log file was created."""
    log_path = "/home/user/rotated_password.log"
    assert os.path.isfile(log_path), f"The file {log_path} does not exist. The binary did not run successfully or the exploit failed."

def test_rotated_password_log_content():
    """Verify that the rotated_password.log contains the correct rotated credentials."""
    log_path = "/home/user/rotated_password.log"
    assert os.path.isfile(log_path), f"The file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "admin:SuperSecret123!"
    assert content == expected_content, f"The content of {log_path} is incorrect. Expected '{expected_content}', got '{content}'."