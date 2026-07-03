# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_cycle_report_content():
    """Verify that the cycle report contains the correct lexicographically ordered cycle."""
    report_path = "/home/user/pipeline/cycle_report.txt"
    assert os.path.exists(report_path), f"Cycle report missing at {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip().replace(" ", "").replace("\n", "")

    expected = "mathservice/algebra,mathservice/geometry"
    assert content == expected, f"Incorrect cycle report. Expected '{expected}', got '{content}'"

def test_go_code_refactored_and_compiles():
    """Verify that the Go code compiles successfully after refactoring."""
    service_dir = "/home/user/service"
    assert os.path.isdir(service_dir), f"Service directory missing at {service_dir}"

    # Run go build
    build_result = subprocess.run(
        ["go", "build", "./..."], 
        cwd=service_dir, 
        capture_output=True, 
        text=True
    )
    assert build_result.returncode == 0, f"'go build ./...' failed:\nStdout: {build_result.stdout}\nStderr: {build_result.stderr}"

def test_go_unit_test_exists_and_passes():
    """Verify that the algebra unit test exists and passes."""
    service_dir = "/home/user/service"
    test_file_path = os.path.join(service_dir, "algebra/algebra_test.go")

    assert os.path.exists(test_file_path), f"Unit test file missing at {test_file_path}"

    # Run go test
    test_result = subprocess.run(
        ["go", "test", "./..."], 
        cwd=service_dir, 
        capture_output=True, 
        text=True
    )
    assert test_result.returncode == 0, f"'go test ./...' failed:\nStdout: {test_result.stdout}\nStderr: {test_result.stderr}"

def test_run_ci_script_executable_and_passes():
    """Verify that the CI bash script exists, is executable, and exits with code 0."""
    script_path = "/home/user/run_ci.sh"

    assert os.path.exists(script_path), f"CI script missing at {script_path}"

    # Check executable permission for the owner
    st = os.stat(script_path)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, f"CI script at {script_path} is not executable"

    # Run the CI script
    ci_result = subprocess.run(
        [script_path], 
        capture_output=True, 
        text=True
    )
    assert ci_result.returncode == 0, f"run_ci.sh failed with exit code {ci_result.returncode}:\nStdout: {ci_result.stdout}\nStderr: {ci_result.stderr}"