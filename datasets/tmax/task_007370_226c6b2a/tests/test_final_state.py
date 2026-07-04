# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/test_restore.sh"
VERIFIER_SRC = "/home/user/verifier.cpp"
VERIFIER_BIN = "/home/user/verifier"
DISK_CHECK_LOG = "/home/user/disk_check.txt"
RESTORE_LOG = "/home/user/restore_log.txt"
PAYLOAD_BIN = "/home/user/restores/payload.bin"

@pytest.fixture(scope="session", autouse=True)
def run_student_script():
    """Run the student's script before checking the final state."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

    # Execute the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_script_executable():
    """Verify the script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"File {SCRIPT_PATH} is missing."
    assert os.access(SCRIPT_PATH, os.X_OK), f"File {SCRIPT_PATH} is not executable."

def test_disk_check_output():
    """Verify disk_check.txt contains df output."""
    assert os.path.isfile(DISK_CHECK_LOG), f"File {DISK_CHECK_LOG} is missing."
    with open(DISK_CHECK_LOG, "r") as f:
        content = f.read()
    assert "Filesystem" in content or "1K-blocks" in content, f"{DISK_CHECK_LOG} does not appear to contain 'df' output."

def test_payload_bin_size():
    """Verify payload.bin exists and is exactly 1024 bytes."""
    assert os.path.isfile(PAYLOAD_BIN), f"File {PAYLOAD_BIN} is missing."
    size = os.path.getsize(PAYLOAD_BIN)
    assert size == 1024, f"File {PAYLOAD_BIN} size is {size} bytes, expected exactly 1024 bytes."

def test_restore_log_content():
    """Verify restore_log.txt contains the correct success message."""
    assert os.path.isfile(RESTORE_LOG), f"File {RESTORE_LOG} is missing."
    with open(RESTORE_LOG, "r") as f:
        content = f.read()
    assert content == "RESTORE VERIFIED: 1024 BYTES\n", f"Incorrect content in {RESTORE_LOG}. Got: {repr(content)}"

def test_no_lingering_verifier_process():
    """Verify that the verifier process exited cleanly and is not running."""
    try:
        # pgrep returns 0 if matches found, 1 if no matches
        result = subprocess.run(["pgrep", "-f", VERIFIER_BIN], capture_output=True, text=True)
        # If result.returncode == 0, processes were found
        assert result.returncode != 0, f"Lingering '{VERIFIER_BIN}' process found. It should have exited cleanly."
    except FileNotFoundError:
        # pgrep not found, fallback to ps
        result = subprocess.run(["ps", "-A"], capture_output=True, text=True)
        assert "verifier" not in result.stdout, "Lingering 'verifier' process found in ps output."