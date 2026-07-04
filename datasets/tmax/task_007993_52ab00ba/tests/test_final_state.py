# test_final_state.py

import os
import subprocess
import time
import json
import pytest

def test_bare_repo_exists():
    """Verify the bare Git repository exists."""
    repo_path = "/home/user/capacity_control.git"
    assert os.path.isdir(repo_path), f"Bare repository directory not found at {repo_path}"

    # Check if it's a bare repo
    config_path = os.path.join(repo_path, "config")
    assert os.path.isfile(config_path), f"Git config not found in {repo_path}"

    with open(config_path, 'r') as f:
        config_content = f.read()
        assert "bare = true" in config_content.lower(), f"Repository at {repo_path} is not configured as bare"

def test_post_receive_hook_exists_and_executable():
    """Verify the post-receive hook exists and is executable."""
    hook_path = "/home/user/capacity_control.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"post-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"post-receive hook at {hook_path} is not executable"

def test_repo_contents_prepared():
    """Verify the trigger_analysis.sh script exists in repo_contents."""
    script_path = "/home/user/repo_contents/trigger_analysis.sh"
    assert os.path.isfile(script_path), f"trigger_analysis.sh not found at {script_path}"

def test_pipeline_execution():
    """Simulate a push to the repository and verify the resulting capacity_report.json."""
    repo_contents = "/home/user/repo_contents"

    # Initialize and push to trigger the pipeline
    subprocess.run(["git", "init"], cwd=repo_contents, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_contents, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_contents, check=True, capture_output=True)

    # Add remote if not exists
    remotes = subprocess.run(["git", "remote"], cwd=repo_contents, capture_output=True, text=True).stdout
    if "origin" not in remotes:
        subprocess.run(["git", "remote", "add", "origin", "/home/user/capacity_control.git"], cwd=repo_contents, check=True, capture_output=True)

    subprocess.run(["git", "add", "."], cwd=repo_contents, check=True, capture_output=True)

    # Commit might fail if there are no changes, but that's fine if it was already committed
    subprocess.run(["git", "commit", "-m", "Test trigger"], cwd=repo_contents, capture_output=True)

    # Push to trigger the hook
    push_result = subprocess.run(
        ["git", "push", "origin", "master"], 
        cwd=repo_contents, 
        capture_output=True, 
        text=True
    )

    # Wait for the pipeline to complete
    report_path = "/home/user/capacity_report.json"
    timeout = 30
    start_time = time.time()

    while time.time() - start_time < timeout:
        if os.path.isfile(report_path):
            break
        time.sleep(1)

    assert os.path.isfile(report_path), f"The file {report_path} was not created within the timeout after pushing."

    # Parse and verify the JSON
    with open(report_path, "r") as f:
        content = f.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"The file {report_path} does not contain valid JSON. Content: {content}")

    assert "cpu_usage" in data, f"'cpu_usage' key not found in {report_path}"
    assert data["cpu_usage"] == 74.5, f"Expected cpu_usage to be 74.5, but got {data['cpu_usage']}"
    assert data.get("status") == "ok", "Expected status to be 'ok'"