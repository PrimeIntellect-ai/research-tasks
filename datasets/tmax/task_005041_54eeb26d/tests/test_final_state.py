# test_final_state.py

import os
import subprocess
import time
import tempfile
import shutil

def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def test_files_and_permissions():
    assert is_executable("/home/user/app_service.sh"), "/home/user/app_service.sh is missing or not executable"
    assert is_executable("/home/user/monitor_bin"), "/home/user/monitor_bin is missing or not executable"
    assert is_executable("/home/user/service.git/hooks/post-receive"), "/home/user/service.git/hooks/post-receive is missing or not executable"

    # Check if bare repo
    assert os.path.isdir("/home/user/service.git/objects"), "/home/user/service.git is not a valid git repository"

def test_git_hook_and_supervisor_behavior():
    # 1. Kill any running instances to ensure a clean state
    subprocess.run(["pkill", "-f", "app_service.sh"])

    # Remove log if exists
    log_path = "/home/user/alert.log"
    if os.path.exists(log_path):
        os.remove(log_path)

    # Create a temp clone
    temp_dir = tempfile.mkdtemp()
    try:
        # Clone the bare repo
        subprocess.run(["git", "clone", "/home/user/service.git", temp_dir], check=True, capture_output=True)

        # First push (Service down)
        with open(os.path.join(temp_dir, "t1.txt"), "w") as f:
            f.write("trigger1\n")

        subprocess.run(["git", "add", "t1.txt"], cwd=temp_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "1"], cwd=temp_dir, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "master"], cwd=temp_dir, check=True, capture_output=True)

        # Give the hook and supervisor a moment to execute
        time.sleep(1)

        # Check log for CRITICAL message and timezone
        assert os.path.exists(log_path), "/home/user/alert.log was not created after the first push"
        with open(log_path, "r") as f:
            log_content1 = f.read()

        assert "CRITICAL: Service was down. Restarted." in log_content1, "CRITICAL message not found in log after first push"
        assert "+0900]" in log_content1, "Timezone +0900 (Asia/Tokyo) not found in log timestamp"

        # Check if service is started
        res = subprocess.run(["pgrep", "-f", "app_service.sh"], capture_output=True)
        assert res.returncode == 0, "app_service.sh is not running after the first push"

        # Second push (Service active)
        with open(os.path.join(temp_dir, "t2.txt"), "w") as f:
            f.write("trigger2\n")

        subprocess.run(["git", "add", "t2.txt"], cwd=temp_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "2"], cwd=temp_dir, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "master"], cwd=temp_dir, check=True, capture_output=True)

        # Give the hook and supervisor a moment to execute
        time.sleep(1)

        with open(log_path, "r") as f:
            log_content2 = f.read()

        assert "INFO: Deployment pushed. Service is active." in log_content2, "INFO message not found in log after second push"

    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        subprocess.run(["pkill", "-f", "app_service.sh"])