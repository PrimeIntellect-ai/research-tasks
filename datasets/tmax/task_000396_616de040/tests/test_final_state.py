# test_final_state.py

import os
import subprocess
import pytest

QA_ENV_DIR = "/home/user/qa_env"
C_FILE = os.path.join(QA_ENV_DIR, "rate_check.c")
EXECUTABLE = os.path.join(QA_ENV_DIR, "rate_check")
VIOLATIONS_LOG = os.path.join(QA_ENV_DIR, "violations.log")
DIFF_LOG = os.path.join(QA_ENV_DIR, "diff.log")

def test_c_file_exists():
    assert os.path.isfile(C_FILE), f"C source file {C_FILE} does not exist."

def test_executable_exists_and_executable():
    assert os.path.isfile(EXECUTABLE), f"Executable file {EXECUTABLE} does not exist."
    assert os.access(EXECUTABLE, os.X_OK), f"File {EXECUTABLE} is not executable."

def test_violations_log_content():
    assert os.path.isfile(VIOLATIONS_LOG), f"Violations log {VIOLATIONS_LOG} does not exist."
    with open(VIOLATIONS_LOG, "r") as f:
        content = f.read().strip().split()

    expected_content = ["11", "14", "15", "20"]
    assert content == expected_content, f"Content of {VIOLATIONS_LOG} does not match expected output. Got: {content}"

def test_diff_log_is_empty():
    assert os.path.isfile(DIFF_LOG), f"Diff log {DIFF_LOG} does not exist."
    assert os.path.getsize(DIFF_LOG) == 0, f"Diff log {DIFF_LOG} is not empty, indicating a mismatch in diff."

def test_rate_check_logic(tmp_path):
    """
    Test the compiled C program with a custom input to ensure the logic is correctly implemented,
    and not just hardcoding the expected output.
    """
    assert os.path.isfile(EXECUTABLE), f"Executable file {EXECUTABLE} does not exist."

    custom_input = "0x00000004\n0x00000001\n0x00000010\n0x00000002\n0x00000003\n"

    try:
        result = subprocess.run(
            [EXECUTABLE],
            input=custom_input,
            text=True,
            capture_output=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Execution of rate_check timed out.")
    except Exception as e:
        pytest.fail(f"Failed to execute rate_check: {e}")

    output = result.stdout.strip().split()
    # Sorted timestamps: 1, 2, 3, 4, 16
    # Diff for index 3 (value 4) -> 4 - 1 = 3 <= 10 (Violation)
    # Diff for index 4 (value 16) -> 16 - 2 = 14 > 10 (OK)
    # Expected violation: 4

    assert output == ["4"], f"Program logic failed on custom input. Expected ['4'], got {output}"