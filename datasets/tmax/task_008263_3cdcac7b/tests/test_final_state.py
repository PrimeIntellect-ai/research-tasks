# test_final_state.py
import os
import stat
import json
import pytest

def test_fetch_secrets_exists():
    """Verify that the fetch_secrets.py script exists."""
    path = "/home/user/fetch_secrets.py"
    assert os.path.isfile(path), f"Expected script {path} does not exist."

def test_prod_secrets_json():
    """Verify the existence, permissions, and content of prod_secrets.json."""
    path = "/home/user/prod_secrets.json"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    # Check permissions
    st = os.stat(path)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o400, f"Permissions for {path} are {oct(mode)}, expected 0o400."

    # Check content
    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} does not contain valid JSON.")

    assert data.get("DB_PASS") == "VaultPass2024!", f"DB_PASS in {path} is incorrect."
    assert data.get("API_KEY") == "SecKey9988", f"API_KEY in {path} is incorrect."

def test_run_app_sh_exists():
    """Verify that the run_app.sh script exists."""
    path = "/home/user/run_app.sh"
    assert os.path.isfile(path), f"Expected script {path} does not exist."

def test_rotation_success_log():
    """Verify the existence and content of rotation_success.log."""
    path = "/home/user/rotation_success.log"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "ROTATION_COMPLETE_882910", f"Content of {path} is incorrect. Got: {content}"