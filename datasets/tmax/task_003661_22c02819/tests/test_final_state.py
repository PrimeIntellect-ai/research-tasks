# test_final_state.py

import os
import subprocess
import pytest

def test_mock_proc_uptime_content():
    mock_file = "/home/user/mock_proc/uptime"
    assert os.path.isfile(mock_file), f"Mock file {mock_file} does not exist"

    with open(mock_file, "r") as f:
        content = f.read().strip()

    assert content == "12345.67 890.12", f"Mock uptime file content is incorrect. Expected '12345.67 890.12', got '{content}'"

def test_workspace_compiles():
    workspace_dir = "/home/user/monitor_workspace"
    assert os.path.isdir(workspace_dir), f"Workspace directory {workspace_dir} does not exist"

    result = subprocess.run(
        ["cargo", "check"],
        cwd=workspace_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Workspace failed to build (cargo check failed):\n{result.stderr}"

def test_cargo_test_results():
    results_file = "/home/user/test_results.txt"
    assert os.path.isfile(results_file), f"Test results file {results_file} does not exist"

    with open(results_file, "r") as f:
        content = f.read()

    assert "test result: ok" in content, "Cargo tests did not pass. 'test result: ok' not found in test_results.txt"

    # Check if at least one test passed
    passed_tests_found = "passed" in content and any(str(i) + " passed" in content for i in range(1, 10))
    assert passed_tests_found, "No tests were executed or recorded as passed in test_results.txt"

def test_circular_dependency_removed():
    core_cargo = "/home/user/monitor_workspace/core/Cargo.toml"
    assert os.path.isfile(core_cargo), f"{core_cargo} does not exist"

    with open(core_cargo, "r") as f:
        content = f.read()

    # The core crate should no longer depend on api
    assert "api =" not in content and '{ path = "../api" }' not in content, "Circular dependency still present in core/Cargo.toml"