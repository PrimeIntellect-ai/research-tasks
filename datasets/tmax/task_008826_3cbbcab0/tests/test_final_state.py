# test_final_state.py

import os
import stat
import subprocess
import pytest

SECRET_KEY_PATH = '/home/user/secret.key'
BIN_ROTATE_PATH = '/home/user/bin/rotate'
ROTATE_LOG_PATH = '/home/user/rotate.log'
EXPECTED_SECRET = 'super_secret_rotation_key_99'
EXPECTED_LOG = 'Credential rotated securely\n'

def test_secret_key_file():
    """Verify /home/user/secret.key exists, has correct content, and 0600 permissions."""
    assert os.path.exists(SECRET_KEY_PATH), f"{SECRET_KEY_PATH} does not exist."
    assert os.path.isfile(SECRET_KEY_PATH), f"{SECRET_KEY_PATH} is not a file."

    with open(SECRET_KEY_PATH, 'r') as f:
        content = f.read().strip()
    assert content == EXPECTED_SECRET, f"Secret key content is incorrect. Expected {EXPECTED_SECRET}, got {content}"

    file_stat = os.stat(SECRET_KEY_PATH)
    mode = stat.S_IMODE(file_stat.st_mode)
    assert mode == 0o600, f"Permissions of {SECRET_KEY_PATH} are not 0600. Got {oct(mode)}"

def test_bin_rotate_executable():
    """Verify /home/user/bin/rotate exists and is executable."""
    assert os.path.exists(BIN_ROTATE_PATH), f"{BIN_ROTATE_PATH} does not exist."
    assert os.path.isfile(BIN_ROTATE_PATH), f"{BIN_ROTATE_PATH} is not a file."
    assert os.access(BIN_ROTATE_PATH, os.X_OK), f"{BIN_ROTATE_PATH} is not executable."

def test_rotate_log_file():
    """Verify /home/user/rotate.log exists and contains the success message."""
    assert os.path.exists(ROTATE_LOG_PATH), f"{ROTATE_LOG_PATH} does not exist."
    assert os.path.isfile(ROTATE_LOG_PATH), f"{ROTATE_LOG_PATH} is not a file."

    with open(ROTATE_LOG_PATH, 'r') as f:
        content = f.read()
    assert content == EXPECTED_LOG, f"Log file content is incorrect. Expected {repr(EXPECTED_LOG)}, got {repr(content)}"

def test_dynamic_security_check():
    """Verify the compiled binary enforces the 0600 permission check on the secret key."""
    # Ensure prerequisites for the test
    assert os.path.exists(SECRET_KEY_PATH), f"Prerequisite {SECRET_KEY_PATH} missing."
    assert os.path.exists(BIN_ROTATE_PATH), f"Prerequisite {BIN_ROTATE_PATH} missing."

    # Backup original permissions
    original_mode = stat.S_IMODE(os.stat(SECRET_KEY_PATH).st_mode)

    try:
        # Change permissions to something insecure
        os.chmod(SECRET_KEY_PATH, 0o644)

        # Remove the log file if it exists
        if os.path.exists(ROTATE_LOG_PATH):
            os.remove(ROTATE_LOG_PATH)

        # Run the executable
        result = subprocess.run([BIN_ROTATE_PATH], capture_output=True, text=True)

        # Check exit code
        assert result.returncode == 1, f"Executable should exit with status 1 for insecure file, got {result.returncode}."

        # Check stderr
        assert "Insecure file" in result.stderr, f"Executable should print 'Insecure file' to stderr, got: {result.stderr}"

        # Check log file is not created
        assert not os.path.exists(ROTATE_LOG_PATH), f"{ROTATE_LOG_PATH} should not be created when permissions are insecure."

    finally:
        # Restore original permissions
        os.chmod(SECRET_KEY_PATH, original_mode)