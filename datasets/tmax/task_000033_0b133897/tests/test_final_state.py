# test_final_state.py
import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/generate_audit.sh"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_script_output_id_2():
    expected_output = (
        "EmployeeName,SystemName,AccessDate,EmployeeClearance,RequiredClearance\n"
        "Charlie Lead,FinanceDB,2023-10-03,3,4\n"
        "Eve Intern,DevServer,2023-10-05,1,2\n"
        "Frank Rogue,CoreInfra,2023-10-06,2,5\n"
        "Dave Worker,CoreInfra,2023-10-07,2,5"
    )

    result = subprocess.run([SCRIPT_PATH, "2"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script exited with non-zero code for ID 2: {result.stderr}"

    actual_output = result.stdout.strip().replace('\r\n', '\n')
    assert actual_output == expected_output, (
        f"Output for ID 2 did not match expected.\n"
        f"Expected:\n{expected_output}\n\n"
        f"Actual:\n{actual_output}"
    )

def test_script_output_id_3():
    expected_output = (
        "EmployeeName,SystemName,AccessDate,EmployeeClearance,RequiredClearance\n"
        "Charlie Lead,FinanceDB,2023-10-03,3,4\n"
        "Eve Intern,DevServer,2023-10-05,1,2\n"
        "Dave Worker,CoreInfra,2023-10-07,2,5"
    )

    result = subprocess.run([SCRIPT_PATH, "3"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script exited with non-zero code for ID 3: {result.stderr}"

    actual_output = result.stdout.strip().replace('\r\n', '\n')
    assert actual_output == expected_output, (
        f"Output for ID 3 did not match expected.\n"
        f"Expected:\n{expected_output}\n\n"
        f"Actual:\n{actual_output}"
    )