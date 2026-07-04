# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_deploy_script_exists_and_executable():
    """Verify that deploy.sh exists and is executable."""
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deployment script {script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deployment script {script_path} is not executable."

def test_analyzer_compiled():
    """Verify that the analyzer binary was compiled and exists."""
    binary_path = "/home/user/analyzer"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    st = os.stat(binary_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Binary {binary_path} is not executable."

def test_backup_archive_exists():
    """Verify that the backup tarball was created."""
    backup_path = "/home/user/billing_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup archive {backup_path} is missing."

def test_cost_report_output():
    """Verify that the cost report output matches expected values."""
    report_path = "/home/user/cost_report.txt"
    assert os.path.isfile(report_path), f"Cost report {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Cost analysis for region: us-east-1",
        "Idle resources found: 1",
        "Potential savings: $45.00"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in cost_report.txt"

def test_deploy_script_idempotent():
    """Verify that running deploy.sh a second time succeeds without error."""
    script_path = "/home/user/deploy.sh"

    # Run the script again
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {script_path} again failed with exit code {result.returncode}. Output: {result.stderr}"

def test_c_program_fixed():
    """Verify the C program was actually fixed."""
    c_path = "/home/user/src/analyzer.c"
    assert os.path.isfile(c_path), f"Source file {c_path} is missing."

    with open(c_path, "r") as f:
        content = f.read()

    assert "getenv" in content, "The typo 'getnv' was not fixed to 'getenv'."
    assert "stdlib.h" in content, "The missing include '<stdlib.h>' was not added."