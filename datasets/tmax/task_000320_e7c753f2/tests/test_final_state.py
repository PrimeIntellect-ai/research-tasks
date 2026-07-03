# test_final_state.py

import os
import subprocess
import pytest

def test_solution_file_exists():
    assert os.path.isfile("/home/user/solution.txt"), "/home/user/solution.txt does not exist."

def test_solution_content():
    solution_path = "/home/user/solution.txt"
    bad_commit_path = "/tmp/.bad_commit"

    assert os.path.isfile(bad_commit_path), "Truth file /tmp/.bad_commit is missing."
    with open(bad_commit_path, "r") as f:
        expected_bad_commit = f.read().strip()

    with open(solution_path, "r") as f:
        content = f.read().strip().splitlines()

    solution_dict = {}
    for line in content:
        if "=" in line:
            key, val = line.split("=", 1)
            solution_dict[key.strip()] = val.strip()

    assert "BAD_COMMIT" in solution_dict, "BAD_COMMIT not found in solution.txt."
    assert solution_dict["BAD_COMMIT"] == expected_bad_commit, f"BAD_COMMIT is incorrect. Expected {expected_bad_commit}, got {solution_dict['BAD_COMMIT']}."

    assert "BUG_FILE" in solution_dict, "BUG_FILE not found in solution.txt."
    assert solution_dict["BUG_FILE"] == "src/math_utils.sh", f"BUG_FILE is incorrect. Expected src/math_utils.sh, got {solution_dict['BUG_FILE']}."

    assert "DROPPED_TX_ID" in solution_dict, "DROPPED_TX_ID not found in solution.txt."
    assert solution_dict["DROPPED_TX_ID"] == "TX_002", f"DROPPED_TX_ID is incorrect. Expected TX_002, got {solution_dict['DROPPED_TX_ID']}."

def test_pipeline_output():
    repo_dir = "/home/user/legacy_pipeline"
    script_path = os.path.join(repo_dir, "run_pipeline.sh")

    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    # Run the pipeline
    result = subprocess.run([script_path], cwd=repo_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"run_pipeline.sh failed with return code {result.returncode}."

    stats_path = os.path.join(repo_dir, "output/stats.txt")
    assert os.path.isfile(stats_path), f"Output file {stats_path} was not generated."

    with open(stats_path, "r") as f:
        stats_content = f.read().strip()

    assert "Average: 2.86" in stats_content, f"Statistics output is incorrect. Expected 'Average: 2.86', got '{stats_content}'."

def test_git_commit_message():
    repo_dir = "/home/user/legacy_pipeline"

    # Check current branch is main
    branch_result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_dir, capture_output=True, text=True)
    assert branch_result.stdout.strip() == "main", f"Expected to be on 'main' branch, but currently on '{branch_result.stdout.strip()}'."

    # Check commit message
    msg_result = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd=repo_dir, capture_output=True, text=True)
    commit_msg = msg_result.stdout.strip()
    assert commit_msg == "Fix statistical anomaly", f"Latest commit message is incorrect. Expected 'Fix statistical anomaly', got '{commit_msg}'."

def test_git_status_clean():
    repo_dir = "/home/user/legacy_pipeline"
    status_result = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir, capture_output=True, text=True)
    assert status_result.stdout.strip() == "", "Git working directory is not clean. Ensure all changes are committed."