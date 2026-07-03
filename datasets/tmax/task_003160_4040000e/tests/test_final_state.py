# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_hash_correct():
    bad_commit_file = "/home/user/bad_commit.txt"
    expected_file = "/tmp/expected_bad_commit.txt"

    assert os.path.exists(bad_commit_file), f"{bad_commit_file} does not exist"
    assert os.path.exists(expected_file), f"{expected_file} does not exist (setup error)"

    with open(bad_commit_file, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected bad commit hash {expected_hash}, but got {actual_hash}"

def test_pipeline_execution_succeeds():
    pipeline_script = "/home/user/risk_app/pipeline.py"
    assert os.path.exists(pipeline_script), f"{pipeline_script} does not exist"

    result = subprocess.run(
        ["python3", pipeline_script],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Pipeline failed to execute. Stderr: {result.stderr}"
    assert "SUCCESS: Pipeline finished" in result.stdout, "Pipeline output did not contain the expected SUCCESS message."

def test_pipeline_code_fixed():
    pipeline_script = "/home/user/risk_app/pipeline.py"
    assert os.path.exists(pipeline_script), f"{pipeline_script} does not exist"

    with open(pipeline_script, "r") as f:
        code = f.read()

    # The fix should add 1e-9 or similar to avoid log(0)
    assert "1e-9" in code or "1e-09" in code or "0.000000001" in code, "Could not find the epsilon value (1e-9) in the pipeline.py script."