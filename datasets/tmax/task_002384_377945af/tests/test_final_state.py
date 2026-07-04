# test_final_state.py

import os
import random
import subprocess
import pytest

def test_leaked_key():
    key_path = "/home/user/leaked_key.txt"
    assert os.path.isfile(key_path), f"File {key_path} does not exist."

    with open(key_path, "r") as f:
        content = f.read().strip()

    expected_key = "AKIA_DIAG_9982AB84C9"
    assert content == expected_key, f"Expected leaked key '{expected_key}', but found '{content}'."

def test_broken_commit():
    commit_file = "/home/user/broken_commit.txt"
    assert os.path.isfile(commit_file), f"File {commit_file} does not exist."

    with open(commit_file, "r") as f:
        content = f.read().strip()

    repo_path = "/home/user/telemetry_pipeline"
    result = subprocess.run(
        ["git", "log", "--format=%H", "--grep=Refactor encoder bitwise logic"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    expected_commit = result.stdout.strip()

    assert expected_commit, "Could not find the expected commit in the git history."
    assert content == expected_commit, f"Expected broken commit hash '{expected_commit}', but found '{content}'."

def test_encoder_fix_fuzz_equivalence():
    agent_script = "/home/user/encoder_fix.py"
    oracle_binary = "/app/telemetry_encoder_working"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(oracle_binary), f"Oracle binary {oracle_binary} does not exist."

    random.seed(42)
    # Using N=1000 to keep test execution time reasonable while still providing strong equivalence guarantees
    test_inputs = [random.randint(-1000000, 1000000) for _ in range(1000)]

    for val in test_inputs:
        val_str = str(val)

        oracle_result = subprocess.run(
            [oracle_binary, val_str],
            capture_output=True,
            text=True
        )
        assert oracle_result.returncode == 0, f"Oracle failed on input {val_str}"
        oracle_output = oracle_result.stdout.strip()

        agent_result = subprocess.run(
            ["python3", agent_script, val_str],
            capture_output=True,
            text=True
        )
        assert agent_result.returncode == 0, f"Agent script failed on input {val_str}. Error: {agent_result.stderr}"
        agent_output = agent_result.stdout.strip()

        assert agent_output == oracle_output, (
            f"Output mismatch on input {val_str}.\n"
            f"Oracle output: '{oracle_output}'\n"
            f"Agent output:  '{agent_output}'"
        )