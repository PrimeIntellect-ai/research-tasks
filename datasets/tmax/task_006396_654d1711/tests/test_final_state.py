# test_final_state.py
import os
import subprocess
import tempfile
import shutil
import pytest

def test_operator_files_exist():
    assert os.path.isfile("/home/user/operator.cpp"), "operator.cpp is missing."
    assert os.path.isfile("/home/user/operator"), "Compiled operator is missing."
    assert os.access("/home/user/operator", os.X_OK), "operator is not executable."

def test_git_hook_exists():
    hook_path = "/home/user/manifests.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} is missing."
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable."

def test_deployment_via_git_push():
    # Create a temporary directory to clone the bare repo
    clone_dir = tempfile.mkdtemp()
    try:
        # Clone the repo
        subprocess.run(["git", "clone", "/home/user/manifests.git", clone_dir], check=True, capture_output=True)

        # Create test manifests
        pod_system = """apiVersion: v1
kind: Pod
metadata:
  name: system-pod
  namespace: kube-system
"""
        pod_default = """apiVersion: v1
kind: Pod
metadata:
  name: default-pod
"""
        pod_monitoring = """apiVersion: v1
kind: Pod
metadata:
  name: monitoring-pod
  namespace: monitoring
"""

        with open(os.path.join(clone_dir, "pod-system.yaml"), "w") as f:
            f.write(pod_system)
        with open(os.path.join(clone_dir, "pod-default.yaml"), "w") as f:
            f.write(pod_default)
        with open(os.path.join(clone_dir, "pod-monitoring.yaml"), "w") as f:
            f.write(pod_monitoring)

        # Commit and push
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clone_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=clone_dir, check=True)
        subprocess.run(["git", "add", "."], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Test commit"], cwd=clone_dir, check=True, capture_output=True)

        # Push should trigger the hook
        push_result = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True, text=True)
        assert push_result.returncode == 0, f"Git push failed: {push_result.stderr}"

        # Verify files are deployed
        assert os.path.isfile("/home/user/deploy/system/pod-system.yaml"), "pod-system.yaml was not deployed to /home/user/deploy/system"
        assert os.path.isfile("/home/user/deploy/default/pod-default.yaml"), "pod-default.yaml was not deployed to /home/user/deploy/default"
        assert os.path.isfile("/home/user/deploy/monitoring/pod-monitoring.yaml"), "pod-monitoring.yaml was not deployed to /home/user/deploy/monitoring"

        # Verify operator.log
        log_path = "/home/user/operator.log"
        assert os.path.isfile(log_path), "operator.log was not created."
        with open(log_path, "r") as f:
            log_content = f.read()

        assert "Deployed pod-system.yaml to /home/user/deploy/system" in log_content, "Missing log entry for pod-system.yaml"
        assert "Deployed pod-default.yaml to /home/user/deploy/default" in log_content, "Missing log entry for pod-default.yaml"
        assert "Deployed pod-monitoring.yaml to /home/user/deploy/monitoring" in log_content, "Missing log entry for pod-monitoring.yaml"

    finally:
        shutil.rmtree(clone_dir)