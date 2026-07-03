# test_final_state.py
import os
import subprocess
import time

def test_push_output_log():
    log_path = "/home/user/push_output.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    # It should contain git push output. We just check it's not empty.
    assert len(content.strip()) > 0, f"{log_path} is empty."

def test_post_receive_hook():
    hook_path = "/home/user/api.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable."

    with open(hook_path, "r") as f:
        content = f.read()

    assert "GIT_WORK_TREE=/home/user/api_app git checkout -f" in content or "git --work-tree=/home/user/api_app checkout -f" in content or "git checkout" in content, "Git hook missing checkout command."
    assert "supervisorctl" in content and "restart all" in content, "Git hook missing supervisorctl restart all command."

def test_metrics_retry_logic():
    metrics_path = "/home/user/local_clone/metrics.py"
    with open(metrics_path, "r") as f:
        content = f.read()

    # Check if there's a loop or retry logic (e.g. range(5), sleep(1), while)
    assert "sleep" in content, "metrics.py does not seem to contain sleep for retries."
    # The original file has no retry loop. We expect something like for/while for retries.
    has_loop = "for " in content or "while " in content
    assert has_loop, "metrics.py does not seem to contain a retry loop."

def test_supervisor_status():
    # Wait a moment to ensure services have had time to start and stabilize
    time.sleep(3)

    result = subprocess.run(
        ["supervisorctl", "-c", "/home/user/supervisord.conf", "status"],
        capture_output=True, text=True
    )

    stdout = result.stdout
    assert "webapp" in stdout, "webapp service not found in supervisorctl status."
    assert "metrics" in stdout, "metrics service not found in supervisorctl status."

    lines = stdout.strip().split("\n")
    for line in lines:
        if "webapp" in line or "metrics" in line:
            assert "RUNNING" in line, f"Service not running. Status line: {line}"

def test_deployed_metrics():
    # Verify that the deployed code matches the local clone (meaning push and hook worked)
    local_metrics = "/home/user/local_clone/metrics.py"
    deployed_metrics = "/home/user/api_app/metrics.py"

    assert os.path.isfile(deployed_metrics), f"{deployed_metrics} does not exist."

    with open(local_metrics, "r") as f:
        local_content = f.read()
    with open(deployed_metrics, "r") as f:
        deployed_content = f.read()

    assert local_content == deployed_content, "Deployed metrics.py does not match the local clone. Did the git push and post-receive hook work?"