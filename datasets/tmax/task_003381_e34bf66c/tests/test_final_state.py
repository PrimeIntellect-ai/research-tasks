# test_final_state.py

import os
import glob
import requests
import stat

def test_git_repo_and_hook_exist():
    """Verify the bare Git repository and post-receive hook exist and are configured."""
    repo_path = "/home/user/config.git"
    hook_path = os.path.join(repo_path, "hooks", "post-receive")

    assert os.path.isdir(repo_path), f"Bare Git repository not found at {repo_path}"
    assert os.path.isfile(hook_path), f"post-receive hook not found at {hook_path}"

    # Check if the hook is executable
    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"post-receive hook at {hook_path} is not executable"

def test_deploy_script_exists():
    """Verify the deployment script exists and is executable."""
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"Deployment script not found at {deploy_script}"

    st = os.stat(deploy_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deployment script at {deploy_script} is not executable"

def test_app_state_directory_exists():
    """Verify the app_state directory exists."""
    app_state = "/home/user/app_state"
    assert os.path.isdir(app_state), f"Working directory not found at {app_state}"

def test_backup_exists():
    """Verify that a backup tarball exists in the BACKUP_DIR."""
    backup_dir = "/home/user/app_backups"
    assert os.path.isdir(backup_dir), f"Backup directory not found at {backup_dir}"

    tar_files = glob.glob(os.path.join(backup_dir, "*.tar"))
    assert len(tar_files) > 0, f"No .tar backup files found in {backup_dir}"

def test_monitoring_service():
    """Verify the monitoring service is running on the correct port and returns the correct token."""
    url = "http://127.0.0.1:8888/status"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the monitoring service at {url}. Error: {e}"

    assert response.status_code == 200, f"Expected HTTP 200 OK, but got {response.status_code}"

    expected_body = "TOKEN=ZULU_XRAY_42"
    actual_body = response.text.strip()
    assert actual_body == expected_body, f"Expected response body '{expected_body}', but got '{actual_body}'"