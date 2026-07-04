# test_final_state.py

import os
import json
import subprocess
import pytest

def test_rust_project_fixed():
    """Verify that the Rust project compiles successfully."""
    rust_dir = "/home/user/rust_target"
    assert os.path.isdir(rust_dir), f"Directory {rust_dir} does not exist."

    # Run cargo build
    result = subprocess.run(["cargo", "build"], cwd=rust_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"Rust project failed to compile. Error:\n{result.stderr}"

def test_rust_project_runs_correctly():
    """Verify that the Rust project runs and prints the expected output."""
    rust_dir = "/home/user/rust_target"
    result = subprocess.run(["cargo", "run"], cwd=rust_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"Rust project failed to run. Error:\n{result.stderr}"
    assert "Hello from the helper!" in result.stdout, "Rust project did not print the expected message."

def test_go_server_fixed():
    """Verify that the Go server no longer splits by pipe."""
    server_go = "/home/user/go_orchestrator/server.go"
    assert os.path.isfile(server_go), f"Missing {server_go}"

    with open(server_go, "r") as f:
        content = f.read()

    assert 'strings.Split(msg, "|")' not in content, "The bug in server.go (splitting by pipe) is still present."

def test_test_script_exists_and_correct():
    """Verify that the test script contains the correct commands."""
    test_script = "/home/user/test_script.txt"
    assert os.path.isfile(test_script), f"Missing {test_script}"

    with open(test_script, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {test_script}, found {len(lines)}"
    assert lines[0] == "BUILD /home/user/rust_target", f"First line in {test_script} is incorrect."
    assert lines[1] == "RUN /home/user/rust_target", f"Second line in {test_script} is incorrect."

def test_e2e_report_valid_and_successful():
    """Verify the e2e JSON report is generated and contains successful results."""
    report_file = "/home/user/e2e_report.json"
    assert os.path.isfile(report_file), f"Missing {report_file}. Did you run the Go client?"

    with open(report_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_file} is not valid JSON.")

    assert isinstance(data, list), f"Expected JSON root to be a list, got {type(data).__name__}"
    assert len(data) == 2, f"Expected exactly 2 results in JSON, got {len(data)}"

    build_res = data[0]
    run_res = data[1]

    assert build_res.get("command") == "BUILD /home/user/rust_target", "First command in report is incorrect."
    assert build_res.get("success") is True, f"BUILD command failed. Output: {build_res.get('output')}"

    assert run_res.get("command") == "RUN /home/user/rust_target", "Second command in report is incorrect."
    assert run_res.get("success") is True, f"RUN command failed. Output: {run_res.get('output')}"
    assert "Hello from the helper!" in run_res.get("output", ""), "RUN command output missing expected message."