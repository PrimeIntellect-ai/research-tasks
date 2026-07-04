# test_final_state.py
import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace"
CI_RUN_SCRIPT = os.path.join(WORKSPACE_DIR, "ci_run.sh")
CI_REPORT = os.path.join(WORKSPACE_DIR, "ci_report.txt")
LIB_SO = os.path.join(WORKSPACE_DIR, "lib", "libverify.so")
CARGO_TOML = os.path.join(WORKSPACE_DIR, "expr_client", "Cargo.toml")
MOCK_API = os.path.join(WORKSPACE_DIR, "mock_api.py")

def test_files_exist():
    """Check that the required files were created."""
    assert os.path.exists(CI_RUN_SCRIPT), f"{CI_RUN_SCRIPT} does not exist."
    assert os.access(CI_RUN_SCRIPT, os.X_OK), f"{CI_RUN_SCRIPT} is not executable."
    assert os.path.exists(LIB_SO), f"{LIB_SO} does not exist."
    assert os.path.exists(CARGO_TOML), f"{CARGO_TOML} does not exist."
    assert os.path.exists(MOCK_API), f"{MOCK_API} does not exist."

def test_ci_run_execution():
    """Run ci_run.sh and verify its output."""
    # Remove the report if it exists to ensure we are testing a fresh run
    if os.path.exists(CI_REPORT):
        os.remove(CI_REPORT)

    # Run the CI script
    try:
        result = subprocess.run(
            [CI_RUN_SCRIPT],
            cwd=WORKSPACE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
            text=True
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {CI_RUN_SCRIPT} timed out.")

    assert result.returncode == 0, f"{CI_RUN_SCRIPT} failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    assert os.path.exists(CI_REPORT), f"{CI_REPORT} was not created by {CI_RUN_SCRIPT}."

    with open(CI_REPORT, "r") as f:
        content = f.read().strip()

    expected_content = "SUCCESS: id=42, valid=true"
    assert content == expected_content, f"Expected '{expected_content}' in {CI_REPORT}, but got '{content}'"