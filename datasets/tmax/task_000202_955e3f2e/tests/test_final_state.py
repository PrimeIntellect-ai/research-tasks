# test_final_state.py

import os
import subprocess
import time
import signal
import pytest

def test_leaked_secret():
    """Verify that the leaked secret was correctly extracted and saved."""
    secret_file = "/home/user/leaked_secret.txt"
    assert os.path.isfile(secret_file), f"File {secret_file} does not exist."

    with open(secret_file, "r") as f:
        content = f.read()

    expected_secret = "SEC_tok_998273645A_leaked"
    assert content == expected_secret, f"Expected content '{expected_secret}', but got '{content}'"

def test_fixed_daemon_exists_and_executable():
    """Verify that the fixed daemon binary exists and is executable."""
    fixed_daemon = "/home/user/fixed_daemon"
    assert os.path.isfile(fixed_daemon), f"File {fixed_daemon} does not exist."
    assert os.access(fixed_daemon, os.X_OK), f"File {fixed_daemon} is not executable."

def test_fixed_daemon_redaction():
    """Verify that the fixed daemon redacts its command-line arguments in /proc."""
    fixed_daemon = "/home/user/fixed_daemon"
    test_secret = "SUPER_SECRET_TEST_TOKEN_999"
    expected_redacted = "*" * len(test_secret)

    # Start the fixed daemon
    process = subprocess.Popen(
        [fixed_daemon, test_secret],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        # Give it a moment to start and execute the redaction
        time.sleep(0.5)

        # Check if process is still running
        if process.poll() is not None:
            pytest.fail("The fixed_daemon exited prematurely. It should sleep/run in the background.")

        cmdline_path = f"/proc/{process.pid}/cmdline"
        assert os.path.exists(cmdline_path), f"Could not find {cmdline_path} for the running process."

        with open(cmdline_path, "rb") as f:
            cmdline_bytes = f.read()

        # The arguments are null-separated
        args = cmdline_bytes.split(b'\0')

        # Filter out empty strings that might appear at the end
        args = [arg for arg in args if arg]

        assert len(args) >= 2, "The process command line does not have the expected number of arguments."

        # The second argument should be the redacted string
        actual_arg = args[1].decode('utf-8', errors='replace')

        assert actual_arg == expected_redacted, (
            f"Command-line argument redaction failed. "
            f"Expected '{expected_redacted}', but found '{actual_arg}'"
        )

    finally:
        # Cleanup: kill the process
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()