# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/cost-analyzer.sh"
CLI_PATH = "/home/user/bin/cloud-cost-cli"
REPORT_PATH = "/home/user/reports/daily_cost.log"

def test_script_execution_success():
    """Test that the script runs successfully in a clean environment and produces the correct output."""
    # Ensure the report file is removed before testing
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

    # Run in a clean environment
    env = {"PATH": "/usr/bin:/bin"}
    result = subprocess.run(["bash", SCRIPT_PATH], env=env, capture_output=True)

    assert result.returncode == 0, f"Script failed with exit code {result.returncode}. Stderr: {result.stderr.decode()}"

    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} was not created."

    with open(REPORT_PATH, "r") as f:
        content = f.read().strip()

    assert content == "Total Cost: $246.75", f"Report content is incorrect. Expected 'Total Cost: $246.75', got '{content}'"

def test_script_error_handling():
    """Test that the script handles a missing CLI tool properly."""
    # Rename the CLI tool to simulate missing dependency
    backup_cli_path = CLI_PATH + ".bak"
    if os.path.exists(CLI_PATH):
        os.rename(CLI_PATH, backup_cli_path)

    try:
        # Run in a clean environment
        env = {"PATH": "/usr/bin:/bin"}
        result = subprocess.run(["bash", SCRIPT_PATH], env=env, capture_output=True)

        assert result.returncode == 1, f"Script should exit with code 1 when CLI is missing, but exited with {result.returncode}."

    finally:
        # Restore the CLI tool
        if os.path.exists(backup_cli_path):
            os.rename(backup_cli_path, CLI_PATH)