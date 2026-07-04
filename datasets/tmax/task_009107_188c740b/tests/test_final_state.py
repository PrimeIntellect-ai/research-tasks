# test_final_state.py
import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/chain_size.sh"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

@pytest.mark.parametrize("backup_id, expected_size", [
    ("bkp_001", "8950"),
    ("bkp_002", "2150"),
    ("bkp_006", "10500"),
    ("bkp_008", "500"),
])
def test_script_output(backup_id, expected_size):
    try:
        result = subprocess.run(
            [SCRIPT_PATH, backup_id],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed when running with {backup_id}. Error: {e.stderr}")

    output = result.stdout.strip()
    assert output == expected_size, (
        f"Expected output for {backup_id} to be '{expected_size}', "
        f"but got '{output}'."
    )