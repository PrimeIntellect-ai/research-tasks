# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace/auth"

def test_mock_s_exists():
    """Check if the assembly file mock.S exists."""
    path = os.path.join(WORKSPACE_DIR, "mock.S")
    assert os.path.isfile(path), f"Assembly file {path} is missing."

def test_main_test_go_exists():
    """Check if the test file main_test.go exists."""
    path = os.path.join(WORKSPACE_DIR, "main_test.go")
    assert os.path.isfile(path), f"Test file {path} is missing."

def test_build_success():
    """Check if the Go package builds successfully, indicating the CGO linking issue is resolved."""
    try:
        result = subprocess.run(
            ["go", "build", "-o", "auth_bin", "main.go"],
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Go build failed. Linking issue might not be resolved.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    bin_path = os.path.join(WORKSPACE_DIR, "auth_bin")
    assert os.path.isfile(bin_path), "The built binary auth_bin was not found."

def test_result_txt_content():
    """Check if result.txt exists and contains exactly '100'."""
    path = os.path.join(WORKSPACE_DIR, "result.txt")
    assert os.path.isfile(path), f"Result file {path} is missing."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "100", f"Expected result.txt to contain '100', but found '{content}'."