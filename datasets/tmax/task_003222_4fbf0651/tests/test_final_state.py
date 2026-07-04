# test_final_state.py
import os
import subprocess
import pytest

TRANSFORM_SCRIPT = "/home/user/transform.sh"
TEST_SCRIPT = "/home/user/test.sh"
PCAP_FILE = "/home/user/traffic.pcap"
EXPECTED_CSV = "/home/user/expected.csv"
DIFF_LOG = "/home/user/diff.log"

def test_transform_sh_correctness():
    """Verify that transform.sh produces the exact expected output."""
    assert os.path.isfile(TRANSFORM_SCRIPT), f"{TRANSFORM_SCRIPT} is missing."
    assert os.access(TRANSFORM_SCRIPT, os.X_OK), f"{TRANSFORM_SCRIPT} is not executable."

    # Run the transform script
    result = subprocess.run(
        [TRANSFORM_SCRIPT, PCAP_FILE],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"transform.sh failed with return code {result.returncode}. Stderr: {result.stderr}"

    # Read expected
    with open(EXPECTED_CSV, "r") as f:
        expected_content = f.read().strip()

    actual_content = result.stdout.strip()

    assert actual_content == expected_content, (
        f"Output of transform.sh does not match {EXPECTED_CSV}.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )

def test_test_sh_exists_and_executable():
    """Verify that test.sh exists and is executable."""
    assert os.path.isfile(TEST_SCRIPT), f"{TEST_SCRIPT} is missing."
    assert os.access(TEST_SCRIPT, os.X_OK), f"{TEST_SCRIPT} is not executable."

def test_test_sh_behavior():
    """Verify that test.sh runs, creates diff.log, and exits with 0 on success."""
    # Clean up diff.log if it exists to ensure test.sh creates it
    if os.path.exists(DIFF_LOG):
        os.remove(DIFF_LOG)

    result = subprocess.run(
        [TEST_SCRIPT],
        capture_output=True,
        text=True,
        cwd="/home/user"
    )

    assert result.returncode == 0, f"test.sh did not exit with code 0. It exited with {result.returncode}. Stderr: {result.stderr}"

    assert os.path.isfile(DIFF_LOG), f"{DIFF_LOG} was not created by test.sh."

    with open(DIFF_LOG, "r") as f:
        diff_content = f.read().strip()

    assert diff_content == "", f"{DIFF_LOG} is not empty. It contains:\n{diff_content}"