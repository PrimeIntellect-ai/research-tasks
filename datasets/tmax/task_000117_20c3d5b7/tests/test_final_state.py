# test_final_state.py
import os
import subprocess
import pytest

REPO_DIR = "/home/user/pipeline_repo"
RECOVERED_DB_PATH = os.path.join(REPO_DIR, "sensor_recovered.db")
BAD_COMMIT_TXT_PATH = "/home/user/bad_commit.txt"
EXPECTED_BAD_COMMIT_TXT = "/tmp/expected_bad_commit.txt"
PROCESS_SH_PATH = os.path.join(REPO_DIR, "process.sh")

def test_recovered_database_exists_and_valid():
    assert os.path.isfile(RECOVERED_DB_PATH), f"Recovered database {RECOVERED_DB_PATH} does not exist."

    result = subprocess.run(
        ["sqlite3", RECOVERED_DB_PATH, "SELECT temp FROM readings;"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to query {RECOVERED_DB_PATH}. Error: {result.stderr}"

    output = result.stdout.strip()
    assert output == "20", f"Expected temp value '20', but got '{output}'."

def test_bad_commit_txt_correct():
    assert os.path.isfile(BAD_COMMIT_TXT_PATH), f"{BAD_COMMIT_TXT_PATH} does not exist."
    assert os.path.isfile(EXPECTED_BAD_COMMIT_TXT), f"Truth file {EXPECTED_BAD_COMMIT_TXT} missing."

    with open(BAD_COMMIT_TXT_PATH, "r") as f:
        actual_sha = f.read().strip()

    with open(EXPECTED_BAD_COMMIT_TXT, "r") as f:
        expected_sha = f.read().strip()

    assert actual_sha == expected_sha, f"Incorrect bad commit SHA. Expected '{expected_sha}', got '{actual_sha}'."

def test_process_sh_fixed():
    assert os.path.isfile(PROCESS_SH_PATH), f"{PROCESS_SH_PATH} does not exist."

    # Run the script with the recovered database
    result = subprocess.run(
        [PROCESS_SH_PATH, RECOVERED_DB_PATH],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"process.sh failed with exit code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}\n"
        f"Make sure the formula is fixed to correctly calculate Fahrenheit."
    )