# test_final_state.py

import os
import subprocess
import pytest

def test_find_deadlocks_script_exists():
    script_path = "/home/user/find_deadlocks.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_script_execution_and_output():
    script_path = "/home/user/find_deadlocks.sh"
    report_path = "/home/user/deadlocks_report.csv"

    # Remove the report if it exists to ensure we are testing the script's output
    if os.path.exists(report_path):
        os.remove(report_path)

    # Run the script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    # Check if the report was created
    assert os.path.isfile(report_path), f"Report file {report_path} was not created by the script."

    # Verify the content of the report
    expected_content = """tx_1,tx_2,resource_1,resource_2
T1,T2,R2,R1
T3,T4,R4,R3
T7,T8,R8,R7"""

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {report_path} is incorrect. Got:\n{content}"