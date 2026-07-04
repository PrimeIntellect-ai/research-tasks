# test_final_state.py
import os
import subprocess

def test_storage_node_builds():
    project_dir = "/home/user/storage-node"
    assert os.path.isdir(project_dir), f"Project directory {project_dir} does not exist"

    build_result = subprocess.run(["cargo", "build"], cwd=project_dir, capture_output=True, text=True)
    assert build_result.returncode == 0, f"Cargo build failed:\n{build_result.stderr}"

def test_storage_node_tests_pass():
    project_dir = "/home/user/storage-node"
    test_result = subprocess.run(["cargo", "test"], cwd=project_dir, capture_output=True, text=True)
    assert test_result.returncode == 0, f"Cargo test failed:\n{test_result.stderr}\n{test_result.stdout}"

def test_ci_workflow_exists_and_valid():
    ci_path = "/home/user/storage-node/.github/workflows/ci.yml"
    assert os.path.isfile(ci_path), f"CI workflow file not found at {ci_path}"

    with open(ci_path, "r") as f:
        ci_content = f.read()

    assert "cargo build" in ci_content, "CI workflow is missing 'cargo build' command"
    assert "cargo test" in ci_content, "CI workflow is missing 'cargo test' command"
    assert "ubuntu-latest" in ci_content, "CI workflow is missing 'ubuntu-latest' specification"

def test_success_log_output():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"Log file not found at {log_path}"

    with open(log_path, "r") as f:
        log_content = f.read()

    expected_string = "Migration and validation successful for block 101"
    assert expected_string in log_content, f"Expected '{expected_string}' in {log_path}, but got:\n{log_content}"