# test_final_state.py
import os
import subprocess
import pytest

REPO_DIR = "/home/user/service_repo"
PROCESSOR_PY = os.path.join(REPO_DIR, "processor.py")
REQUIREMENTS_TXT = os.path.join(REPO_DIR, "requirements.txt")
SECRET_BAD_COMMIT = "/home/user/.secret_bad_commit"
BUG_INFO_TXT = "/home/user/bug_info.txt"

def test_bug_info_txt():
    assert os.path.isfile(SECRET_BAD_COMMIT), f"Secret file {SECRET_BAD_COMMIT} missing."
    with open(SECRET_BAD_COMMIT, "r") as f:
        expected_hash = f.read().strip()

    assert os.path.isfile(BUG_INFO_TXT), f"{BUG_INFO_TXT} does not exist."
    with open(BUG_INFO_TXT, "r") as f:
        content = f.read().strip()

    expected_content = f"Bad Commit: {expected_hash}"
    assert expected_content in content, f"Expected '{expected_content}' in {BUG_INFO_TXT}, but got '{content}'."

def test_requirements_fixed():
    assert os.path.isfile(REQUIREMENTS_TXT), f"{REQUIREMENTS_TXT} does not exist."
    with open(REQUIREMENTS_TXT, "r") as f:
        content = f.read()
    assert "nonexistent-fake-package" not in content, "The nonexistent-fake-package dependency is still in requirements.txt."

def test_processor_runs():
    assert os.path.isfile(PROCESSOR_PY), f"{PROCESSOR_PY} does not exist."
    try:
        result = subprocess.run(
            ["python3", PROCESSOR_PY],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("processor.py timed out after 5 seconds. The infinite loop bug is likely not fixed.")

    assert result.returncode == 0, f"processor.py failed with return code {result.returncode}."
    assert "Service finished successfully." in result.stdout, "processor.py did not output the expected success message."