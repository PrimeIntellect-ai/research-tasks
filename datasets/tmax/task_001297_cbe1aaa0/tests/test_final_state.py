# test_final_state.py
import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_app_compiled_and_executable():
    app_path = os.path.join(PROJECT_DIR, "app")
    assert os.path.isfile(app_path), f"Executable {app_path} was not found. Did you run make?"
    assert os.access(app_path, os.X_OK), f"File {app_path} is not executable."

def test_app_output():
    app_path = os.path.join(PROJECT_DIR, "app")
    try:
        result = subprocess.run([app_path], capture_output=True, text=True, check=True)
        assert result.stdout == "Result: 44\n", f"Expected output 'Result: 44\\n', got {repr(result.stdout)}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running {app_path} failed with exit code {e.returncode}")

def test_test_deploy_script_exists():
    script_path = os.path.join(PROJECT_DIR, "test_deploy.py")
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist."

def test_status_log_exists_and_correct():
    log_path = os.path.join(PROJECT_DIR, "status.log")
    assert os.path.isfile(log_path), f"Status log {log_path} does not exist. Did you run the Python script?"

    with open(log_path, "rb") as f:
        content = f.read()

    # It should be UTF-16LE. It might have a BOM.
    # UTF-16LE for 'DEPLOY_READY'
    expected_no_bom = "DEPLOY_READY".encode("utf-16le")
    expected_with_bom = "DEPLOY_READY".encode("utf-16")

    assert content in (expected_no_bom, expected_with_bom), (
        "status.log does not contain the correctly UTF-16LE encoded string 'DEPLOY_READY'."
    )

def test_github_actions_workflow():
    workflow_path = os.path.join(PROJECT_DIR, ".github", "workflows", "ci.yml")
    assert os.path.isfile(workflow_path), f"GitHub Actions workflow file {workflow_path} does not exist."

    with open(workflow_path, "r") as f:
        content = f.read()

    assert "python3 test_deploy.py" in content, (
        f"Workflow file {workflow_path} does not contain the command 'python3 test_deploy.py'."
    )

    # Basic structural check for YAML (without using external yaml parser)
    assert "jobs:" in content, "Workflow file does not seem to contain 'jobs:'."
    assert "test:" in content or "test" in content, "Workflow file does not seem to contain a 'test' job."
    assert "steps:" in content, "Workflow file does not seem to contain 'steps:'."