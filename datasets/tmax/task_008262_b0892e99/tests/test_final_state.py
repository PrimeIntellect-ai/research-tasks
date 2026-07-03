# test_final_state.py

import os
import subprocess

def test_bug_commit_hash():
    # Retrieve the actual buggy commit hash from git history
    result = subprocess.run(
        ["git", "log", "--grep=Refactor JD calculation for performance", "--format=%H"],
        cwd="/home/user/astro_calc",
        capture_output=True,
        text=True,
        check=True
    )
    expected_hash = result.stdout.strip()
    assert expected_hash, "Could not find the buggy commit in git history"

    bug_commit_file = "/home/user/bug_commit.txt"
    assert os.path.isfile(bug_commit_file), f"{bug_commit_file} does not exist"

    with open(bug_commit_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected buggy commit hash {expected_hash}, but found {actual_hash}"

def test_secret_recovered():
    secret_file = "/home/user/secret.txt"
    assert os.path.isfile(secret_file), f"{secret_file} does not exist"

    with open(secret_file, "r") as f:
        secret = f.read().strip()

    assert secret == "7b9a2c8f-3e1d-4a5b-8c2e-1d9f4a5b8c2e", "The recovered secret token is incorrect"

def test_jd_output():
    output_file = "/home/user/jd_output.txt"
    assert os.path.isfile(output_file), f"{output_file} does not exist"

    with open(output_file, "r") as f:
        output = f.read().strip()

    # The expected output is 2460311.0 for 2024-01-01 12:00:00
    assert output == "2460311.0", f"Expected JD output to be 2460311.0, but got {output}"

def test_jd_py_fixed():
    jd_file = "/home/user/astro_calc/jd.py"
    assert os.path.isfile(jd_file), f"{jd_file} does not exist"

    with open(jd_file, "r") as f:
        content = f.read()

    assert "term3 = int((275 * M) / 9)" in content, "jd.py does not contain the corrected formula (division by 9)"
    assert "term3 = int((275 * M) / 8)" not in content, "jd.py still contains the buggy formula (division by 8)"

def test_test_jd_passes():
    # Ensure that the test_jd.py test passes after the fix
    result = subprocess.run(
        ["python3", "test_jd.py"],
        cwd="/home/user/astro_calc",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"test_jd.py failed to run successfully:\n{result.stderr}"
    assert "Tests passed" in result.stdout, "test_jd.py did not output 'Tests passed'"