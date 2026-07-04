# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_hash():
    expected_file = "/tmp/expected_bad_commit.txt"
    user_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(expected_file), f"Truth file {expected_file} is missing."
    assert os.path.isfile(user_file), f"User file {user_file} is missing. Did you save the bad commit hash?"

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(user_file, "r") as f:
        user_hash = f.read().strip()

    assert user_hash == expected_hash, f"Expected bad commit hash {expected_hash}, but got {user_hash}"

def test_fixed_output_file():
    user_output_file = "/home/user/fixed_output.txt"
    assert os.path.isfile(user_output_file), f"User output file {user_output_file} is missing."

    with open(user_output_file, "r") as f:
        output_val = f.read().strip()

    expected_output = "1.9212441"
    assert output_val == expected_output, f"Expected output {expected_output}, but got {output_val} in {user_output_file}."

def test_script_is_fixed():
    repo_dir = "/home/user/repo"
    process_script = os.path.join(repo_dir, "process.sh")

    assert os.path.isfile(process_script), f"Script {process_script} is missing."

    # Run the script and check its output
    try:
        result = subprocess.run(
            ["./process.sh"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True
        )
        script_output = result.stdout.strip()
        expected_output = "1.9212441"
        assert script_output == expected_output, f"The script ./process.sh output {script_output}, expected {expected_output}. The bug is not fixed."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run ./process.sh: {e.stderr}")