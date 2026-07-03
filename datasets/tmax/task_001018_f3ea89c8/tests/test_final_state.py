# test_final_state.py

import os
import stat
import subprocess

def test_hook_exists_and_executable():
    hook_path = "/home/user/operator-repo/.git/hooks/post-commit"
    assert os.path.isfile(hook_path), f"Git hook file does not exist at {hook_path}"

    st = os.stat(hook_path)
    assert st.st_mode & stat.S_IXUSR, f"Git hook file at {hook_path} is not executable"

def test_hook_behavior():
    repo_path = "/home/user/operator-repo"
    manifest_path = os.path.join(repo_path, "manifest.yaml")
    log_path = "/home/user/operator.log"
    alert_path = "/home/user/alerts.mail"

    # Ensure a clean slate for the test
    if os.path.exists(log_path):
        os.remove(log_path)
    if os.path.exists(alert_path):
        os.remove(alert_path)

    # --- Test normal commit (replicas = 3) ---
    manifest_content_3 = "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: test-app\nspec:\n  replicas: 3\n"
    with open(manifest_path, "w") as f:
        f.write(manifest_content_3)

    subprocess.run(["git", "add", "manifest.yaml"], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Update to 3"], cwd=repo_path, check=True)

    assert os.path.isfile(log_path), f"Log file {log_path} was not created after commit."
    with open(log_path, "r") as f:
        log_content = f.read()
    assert "DEPLOY: replicas=3" in log_content, f"Expected 'DEPLOY: replicas=3' in {log_path}"

    if os.path.exists(alert_path):
        with open(alert_path, "r") as f:
            alert_content = f.read()
        assert "ALERT: High replica count detected (3)" not in alert_content, "Alert should NOT be generated for replicas=3"

    # --- Test alert commit (replicas = 8) ---
    manifest_content_8 = "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: test-app\nspec:\n  replicas: 8\n"
    with open(manifest_path, "w") as f:
        f.write(manifest_content_8)

    subprocess.run(["git", "add", "manifest.yaml"], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Update to 8"], cwd=repo_path, check=True)

    with open(log_path, "r") as f:
        log_content = f.read()
    assert "DEPLOY: replicas=8" in log_content, f"Expected 'DEPLOY: replicas=8' in {log_path}"

    assert os.path.isfile(alert_path), f"Alert file {alert_path} was not created after high-replica commit."
    with open(alert_path, "r") as f:
        alert_content = f.read()
    assert "ALERT: High replica count detected (8)" in alert_content, f"Expected 'ALERT: High replica count detected (8)' in {alert_path}"