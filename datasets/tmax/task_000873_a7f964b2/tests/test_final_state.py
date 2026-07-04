# test_final_state.py
import os
import re
import subprocess
import math
import pytest

def get_output(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command '{cmd}' failed with return code {result.returncode}. Stderr: {result.stderr}")
    try:
        return float(result.stdout.strip())
    except ValueError:
        raise ValueError(f"Could not parse output of '{cmd}' as float. Output was: {result.stdout.strip()}")

def test_bad_commit_file():
    bad_commit_path = "/home/user/bad_commit.txt"
    assert os.path.isfile(bad_commit_path), f"File {bad_commit_path} does not exist."

    with open(bad_commit_path, "r") as f:
        content = f.read().strip()

    assert re.match(r"^[0-9a-f]{40}$", content), f"File {bad_commit_path} does not contain a valid 40-character git commit hash. Found: '{content}'"

def test_pipeline_output_matches_oracle():
    oracle_val = get_output("/app/oracle_bin")
    agent_val = get_output("cd /home/user/pipeline_repo && python3 process_data.py")

    error = abs(oracle_val - agent_val)
    threshold = 1e-5

    assert error <= threshold, f"Numerical output mismatch! Oracle: {oracle_val}, Agent: {agent_val}, Absolute Error: {error} (Threshold: {threshold})"