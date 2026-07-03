# test_final_state.py
import os
import subprocess

def test_test_results_log():
    """
    Check that test_results.log exists and contains 'PASS'.
    """
    log_path = "/home/user/workspace/test_results.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "PASS" in content, f"Expected 'PASS' in {log_path}, but it was not found."

def test_ids_alerts_log():
    """
    Check that ids_alerts.log exists and contains the correct alert string.
    """
    log_path = "/home/user/workspace/ids_alerts.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    expected_alert = "[ALERT] Path traversal attempt blocked for filename:"
    assert expected_alert in content, f"Expected '{expected_alert}' in {log_path}, but it was not found."

def test_go_files_exist():
    """
    Check that the required Go files exist.
    """
    required_files = [
        "/home/user/workspace/server.go",
        "/home/user/workspace/middleware.go",
        "/home/user/workspace/server_test.go",
        "/home/user/workspace/go.mod",
    ]
    for file_path in required_files:
        assert os.path.isfile(file_path), f"Required file {file_path} is missing."

def test_go_tests_pass():
    """
    Run 'go test' in the workspace directory and ensure it passes.
    """
    workspace_path = "/home/user/workspace"
    result = subprocess.run(
        ["go", "test"],
        cwd=workspace_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'go test' failed with output:\n{result.stdout}\n{result.stderr}"