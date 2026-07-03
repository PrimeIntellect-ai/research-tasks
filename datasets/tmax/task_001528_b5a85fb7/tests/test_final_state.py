# test_final_state.py

import os
import subprocess
import pytest

LEAKED_TX_PATH = "/home/user/leaked_tx.txt"
PATCH_PATH = "/home/user/fix.patch"
SERVICE_DIR = "/home/user/service"

def test_leaked_tx_file():
    assert os.path.isfile(LEAKED_TX_PATH), f"File {LEAKED_TX_PATH} does not exist."
    with open(LEAKED_TX_PATH, "r") as f:
        content = f.read().strip()

    expected = "ERR_TX_99482A"
    assert content == expected, f"Expected {LEAKED_TX_PATH} to contain '{expected}', but found '{content}'."

def test_patch_file_exists_and_format():
    assert os.path.isfile(PATCH_PATH), f"File {PATCH_PATH} does not exist."
    with open(PATCH_PATH, "r") as f:
        content = f.read()

    assert "---" in content and "+++" in content, f"{PATCH_PATH} does not look like a unified diff."
    assert "free" in content, f"The patch does not seem to contain a call to free()."

def test_valgrind_no_leaks():
    assert os.path.isdir(SERVICE_DIR), f"Directory {SERVICE_DIR} does not exist."

    # Recompile the service
    try:
        subprocess.run(["make", "clean"], cwd=SERVICE_DIR, check=True, capture_output=True)
        subprocess.run(["make"], cwd=SERVICE_DIR, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile the service:\n{e.stderr.decode('utf-8')}")

    # Ensure the executable exists
    exe_path = os.path.join(SERVICE_DIR, "tx_service")
    assert os.path.isfile(exe_path), f"Executable {exe_path} was not built."

    # Run valgrind
    try:
        result = subprocess.run(
            ["valgrind", "--leak-check=full", "--error-exitcode=1", "./tx_service"],
            cwd=SERVICE_DIR,
            capture_output=True,
            text=True,
            check=False
        )
    except FileNotFoundError:
        pytest.fail("valgrind is not installed or not in PATH.")

    stderr = result.stderr

    # Check valgrind output for leak absence
    no_leaks_msg1 = "All heap blocks were freed -- no leaks are possible"
    no_leaks_msg2 = "definitely lost: 0 bytes in 0 blocks"

    if no_leaks_msg1 not in stderr and no_leaks_msg2 not in stderr:
        pytest.fail(f"Memory leak detected or valgrind failed. Valgrind output:\n{stderr}")

    # Ensure valgrind didn't exit with an error code (due to memory errors)
    assert result.returncode == 0, f"Valgrind reported errors:\n{stderr}"