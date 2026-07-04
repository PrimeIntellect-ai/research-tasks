# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_unlocked_rsa_exists_and_permissions():
    path = "/home/user/unlocked_rsa"
    assert os.path.exists(path), f"Missing file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

    # SSH keys must have strict permissions to be used, typically 0600 or 0400
    st = os.stat(path)
    # Check that group and others have no permissions
    assert not bool(st.st_mode & (stat.S_IRWXG | stat.S_IRWXO)), \
        f"Permissions for {path} are too open. Should not be accessible by group/others."

def test_payload_exists():
    path = "/home/user/payload.py"
    assert os.path.exists(path), f"Missing file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

def test_payload_execution_and_size():
    payload_path = "/home/user/payload.py"
    assert os.path.exists(payload_path), "Payload script does not exist."

    # Execute the payload and capture output
    try:
        out = subprocess.check_output(
            ["python3", payload_path], 
            stderr=subprocess.STDOUT, 
            timeout=10
        ).decode()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Payload script execution failed with return code {e.returncode}. Output:\n{e.output.decode(errors='ignore')}")
    except subprocess.TimeoutExpired:
        pytest.fail("Payload script execution timed out.")
    except Exception as e:
        pytest.fail(f"Failed to execute payload script: {e}")

    assert "FLAG{" in out, f"Payload output did not contain the expected flag format. Output was: {out}"

    # Metric constraint check
    size = os.path.getsize(payload_path)
    threshold = 110
    assert size <= threshold, f"Payload size {size} bytes exceeds the threshold of {threshold} bytes."