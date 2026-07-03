# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_fstab_configuration():
    """Verify the fstab file exists and contains the correct configuration."""
    fstab_path = "/home/user/app_storage.fstab"
    assert os.path.exists(fstab_path), f"{fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    # Parse the line
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
    assert len(lines) == 1, f"{fstab_path} should contain exactly one valid fstab line."

    parts = lines[0].split()
    assert len(parts) == 6, f"fstab line does not have 6 fields: {lines[0]}"

    assert parts[0] == "UUID=9b1c990b-8f19-4b6d-9799-a3b043b177d4", "Incorrect UUID."
    assert parts[1] == "/home/user/app_data", "Incorrect mount point."
    assert parts[2] == "ext4", "Incorrect filesystem type."
    assert parts[3] == "defaults,nofail", "Incorrect mount options."
    assert parts[4] == "0", "Incorrect dump number."
    assert parts[5] == "2", "Incorrect pass number."

def test_app_data_directory_exists():
    """Verify the app_data directory exists."""
    assert os.path.isdir("/home/user/app_data"), "/home/user/app_data directory does not exist."

def test_git_bare_repo_and_hook():
    """Verify the bare Git repository and the post-receive hook."""
    repo_dir = "/home/user/deploy.git"
    assert os.path.isdir(repo_dir), f"{repo_dir} does not exist."

    # Check if it's a bare repo
    result = subprocess.run(["git", "-C", repo_dir, "rev-parse", "--is-bare-repository"], capture_output=True, text=True)
    assert result.stdout.strip() == "true", f"{repo_dir} is not a bare Git repository."

    hook_path = os.path.join(repo_dir, "hooks", "post-receive")
    assert os.path.exists(hook_path), f"Git hook {hook_path} does not exist."

    # Check if executable
    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Git hook {hook_path} is not executable."

    with open(hook_path, "r") as f:
        hook_content = f.read()

    assert "checkout" in hook_content and "main" in hook_content, "Hook does not seem to checkout the main branch."
    assert "/home/user/app_src" in hook_content, "Hook does not specify the correct working tree directory."
    assert "systemctl --user restart app-worker.service" in hook_content or "systemctl --user restart app-worker" in hook_content, "Hook does not restart the app-worker service."

def test_systemd_service_file():
    """Verify the systemd service file configuration."""
    service_path = "/home/user/.config/systemd/user/app-worker.service"
    assert os.path.exists(service_path), f"{service_path} does not exist."

    with open(service_path, "r") as f:
        content = f.read()

    assert "Restart=on-failure" in content, "Service file missing 'Restart=on-failure'."
    assert "podman run" in content, "Service file missing 'podman run' command."
    assert "-v /home/user/app_src:/app" in content or "--volume /home/user/app_src:/app" in content or "--volume=/home/user/app_src:/app" in content, "Service file missing volume mount for /app."
    assert "-v /home/user/app_data:/data" in content or "--volume /home/user/app_data:/data" in content or "--volume=/home/user/app_data:/data" in content, "Service file missing volume mount for /data."
    assert "python:3.10-alpine" in content, "Service file missing the correct container image."
    assert "python /app/main.py" in content, "Service file missing the correct execution command."

def test_service_is_active():
    """Verify that the systemd service is active."""
    result = subprocess.run(["systemctl", "--user", "is-active", "app-worker.service"], capture_output=True, text=True)
    assert result.stdout.strip() == "active", "app-worker.service is not active."

def test_podman_container_running():
    """Verify that the podman container is running."""
    result = subprocess.run(["podman", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
    containers = result.stdout.strip().splitlines()
    assert "app-worker" in containers, "Podman container 'app-worker' is not running."

def test_deploy_log_content():
    """Verify the deploy log exists and contains the correct message."""
    log_path = "/home/user/app_data/deploy_log.txt"
    assert os.path.exists(log_path), f"{log_path} does not exist. The pipeline might not have triggered successfully."

    with open(log_path, "r") as f:
        content = f.read()

    assert "Update deployed successfully" in content, f"Expected message not found in {log_path}."