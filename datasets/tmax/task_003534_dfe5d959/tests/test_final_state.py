# test_final_state.py

import os
import subprocess
import re
import pytest

def test_resolution_file_exists():
    path = "/home/user/resolution.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The task was not completed properly."

def test_resolution_content():
    path = "/home/user/resolution.txt"
    hash_path = "/tmp/.bad_commit_hash"

    assert os.path.isfile(hash_path), "The bad commit hash file is missing."
    with open(hash_path, "r") as f:
        expected_hash = f.read().strip()

    with open(path, "r") as f:
        content = f.read()

    bad_commit_match = re.search(r"BAD_COMMIT=([a-f0-9]{40})", content)
    assert bad_commit_match is not None, "BAD_COMMIT with a 40-character hash not found in resolution.txt."
    actual_hash = bad_commit_match.group(1)

    assert actual_hash == expected_hash, f"Incorrect BAD_COMMIT. Expected {expected_hash}, got {actual_hash}."

    avg_match = re.search(r"CORRECTED_AVERAGE=([0-9.]+)", content)
    assert avg_match is not None, "CORRECTED_AVERAGE not found in resolution.txt."
    actual_avg = avg_match.group(1)

    assert actual_avg == "83.71", f"Incorrect CORRECTED_AVERAGE. Expected 83.71, got {actual_avg}."

def test_calc_py_output():
    repo_path = "/home/user/metric_service"
    calc_path = os.path.join(repo_path, "calc.py")

    assert os.path.isfile(calc_path), f"{calc_path} does not exist."

    try:
        result = subprocess.run(
            ["python3", "calc.py"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        assert "Final Average: 83.71" in output, f"calc.py did not output the correct final average. Output was: {output}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running calc.py failed with error: {e.stderr}")

def test_git_bisect_aborted():
    repo_path = "/home/user/metric_service"
    bisect_start_path = os.path.join(repo_path, ".git", "BISECT_START")

    assert not os.path.exists(bisect_start_path), "git bisect is still active. You must abort the bisect operation."