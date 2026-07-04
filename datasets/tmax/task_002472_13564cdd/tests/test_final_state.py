# test_final_state.py

import os
import stat
import requests
import pytest

def test_setup_script_exists_and_executable():
    script_path = "/home/user/setup_and_run.sh"
    assert os.path.isfile(script_path), f"Setup script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Setup script {script_path} is not executable."

def test_provisioner_service_and_side_effects():
    # Make the request to the provisioner service
    url = "http://127.0.0.1:8080/provision"
    params = {
        "username": "testuser1",
        "ip": "192.168.5.5"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the provisioner service on 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"
    assert response.text.strip() == "OK", f"Expected response body 'OK', got '{response.text}'"

    # Verify side effects
    base_dir = "/home/user/managed_users/testuser1"
    www_dir = "/home/user/public_web/testuser1"
    symlink_path = os.path.join(base_dir, "www")
    route_file = os.path.join(base_dir, "route.sh")

    assert os.path.isdir(base_dir), f"Directory {base_dir} was not created."
    assert os.path.isdir(www_dir), f"Directory {www_dir} was not created."

    assert os.path.islink(symlink_path), f"Symlink {symlink_path} was not created."
    target = os.readlink(symlink_path)
    assert target == www_dir, f"Symlink {symlink_path} points to {target}, expected {www_dir}."

    assert os.path.isfile(route_file), f"File {route_file} was not created."
    with open(route_file, "r") as f:
        content = f.read().strip()

    expected_content = "ip route add 192.168.5.5 via 10.0.0.1"
    assert content == expected_content, f"File {route_file} content mismatch. Expected '{expected_content}', got '{content}'."