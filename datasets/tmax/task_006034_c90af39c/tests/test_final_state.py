# test_final_state.py
import os
import json
import subprocess
import pytest

def test_symlink_active_data():
    """Verify /home/user/app/active_data is a symlink pointing to /home/user/app/data."""
    symlink_path = "/home/user/app/active_data"
    expected_target = "/home/user/app/data"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink or does not exist."

    target = os.readlink(symlink_path)
    # The student might use an absolute path or a relative path that resolves to the correct directory.
    # We will check if it resolves to the correct absolute path.
    abs_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
    assert abs_target == expected_target, f"Symlink points to {abs_target}, expected {expected_target}."

def test_service_b_port_fixed():
    """Verify service_b.py has been modified to use port 8000."""
    service_b_path = "/home/user/src/service_b.py"
    assert os.path.isfile(service_b_path), f"{service_b_path} does not exist."

    with open(service_b_path, "r") as f:
        content = f.read()

    assert "127.0.0.1:8000" in content, "service_b.py does not contain the corrected port 8000."
    assert "127.0.0.1:9090" not in content, "service_b.py still contains the misconfigured port 9090."

def test_supervisord_running():
    """Verify supervisord is running."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "supervisord"]).decode("utf-8").strip()
        assert output, "supervisord process not found."
    except subprocess.CalledProcessError:
        pytest.fail("supervisord is not running.")

def test_pipeline_success_file():
    """Verify pipeline_success.json exists and contains the correct data."""
    success_file_path = "/home/user/app/data/pipeline_success.json"
    assert os.path.isfile(success_file_path), f"Success file {success_file_path} is missing. Network issue not fixed or services not running properly."

    with open(success_file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {success_file_path} does not contain valid JSON.")

    assert data.get("result") == "success", "JSON 'result' is not 'success'."
    assert data.get("source") == "pipeline_ready", "JSON 'source' is not 'pipeline_ready'."