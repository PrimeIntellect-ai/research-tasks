# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_txt():
    bad_commit_file = "/home/user/bad_commit.txt"
    expected_commit_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(bad_commit_file), f"The file {bad_commit_file} does not exist. Did you record your findings?"
    assert os.path.isfile(expected_commit_file), f"The truth file {expected_commit_file} is missing."

    with open(bad_commit_file, "r") as f:
        actual_commit = f.read().strip()

    with open(expected_commit_file, "r") as f:
        expected_commit = f.read().strip()

    assert actual_commit == expected_commit, f"The bad commit hash in {bad_commit_file} is incorrect. Expected {expected_commit}, got {actual_commit}."

def test_formula_fixed():
    main_rs = "/home/user/collatz-calc/src/main.rs"
    assert os.path.isfile(main_rs), f"The file {main_rs} does not exist."

    with open(main_rs, "r") as f:
        content = f.read()

    assert "n = 3 * n + 1;" in content, "The formula in src/main.rs was not correctly reverted to 'n = 3 * n + 1;'."
    assert "n = 3 * n - 1;" not in content, "The incorrect formula 'n = 3 * n - 1;' is still present in src/main.rs."

def test_cargo_run_success():
    project_dir = "/home/user/collatz-calc"
    assert os.path.isdir(project_dir), f"Project directory {project_dir} is missing."

    try:
        result = subprocess.run(
            ["cargo", "run", "--", "17"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Running 'cargo run -- 17' timed out. The infinite loop is likely still present.")

    assert result.returncode == 0, f"cargo run failed for input 17. Exit code: {result.returncode}\nStderr: {result.stderr}"