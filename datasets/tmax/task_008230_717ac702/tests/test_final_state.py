# test_final_state.py
import os
import subprocess

def test_audit_report_content():
    report_path = "/home/user/vulnerable_crates.txt"
    assert os.path.isfile(report_path), f"Audit report not found at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["api", "auth", "db", "ui"]
    assert lines == expected, f"Audit report content is incorrect. Expected {expected}, got {lines}"

def test_cargo_test_passes():
    workspace_dir = "/home/user/ci_workspace"
    assert os.path.isdir(workspace_dir), f"Workspace directory not found at {workspace_dir}"

    result = subprocess.run(
        ["cargo", "test", "--workspace"],
        cwd=workspace_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"cargo test failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"