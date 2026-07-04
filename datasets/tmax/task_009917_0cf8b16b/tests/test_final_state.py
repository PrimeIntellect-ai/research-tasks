# test_final_state.py

import os
import stat
import pwd

def test_rollout_script_exists_and_executable():
    script_path = "/home/user/rollout.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_deployments_created():
    # Read targets.conf to determine what should have been created
    targets_path = "/home/user/targets.conf"
    assert os.path.isfile(targets_path), f"File {targets_path} is missing."

    with open(targets_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    valid_users = []
    invalid_users = []

    for line in lines:
        if ":" in line:
            dir_name, username = line.split(":", 1)
            try:
                pwd.getpwnam(username)
                valid_users.append((dir_name, username))
            except KeyError:
                invalid_users.append((dir_name, username))

    # Check valid users deployments
    for dir_name, username in valid_users:
        status_file = f"/home/user/deployments/{dir_name}/status.txt"
        assert os.path.isfile(status_file), f"Expected status file missing: {status_file}"
        with open(status_file, "r") as f:
            content = f.read().strip()
        assert content == f"deployed_for_{username}", f"Incorrect content in {status_file}. Expected 'deployed_for_{username}', got '{content}'."

    # Check invalid users in error log
    error_log_path = "/home/user/rollout_errors.log"
    if invalid_users:
        assert os.path.isfile(error_log_path), f"Error log {error_log_path} is missing."
        with open(error_log_path, "r") as f:
            log_content = f.read()

        for dir_name, username in invalid_users:
            expected_error = f"Failed: {dir_name} - {username} not found"
            assert expected_error in log_content, f"Expected error '{expected_error}' not found in {error_log_path}."

def test_systemd_service_file():
    service_path = "/home/user/.config/systemd/user/rollout.service"
    assert os.path.isfile(service_path), f"Service file {service_path} is missing."

    with open(service_path, "r") as f:
        content = f.read()

    assert "[Unit]" in content, f"[Unit] section missing in {service_path}"
    assert "Description=Rollout Service" in content, f"'Description=Rollout Service' missing in {service_path}"
    assert "[Service]" in content, f"[Service] section missing in {service_path}"
    assert "Type=oneshot" in content, f"'Type=oneshot' missing in {service_path}"
    assert "ExecStart=/home/user/rollout.py" in content, f"'ExecStart=/home/user/rollout.py' missing in {service_path}"