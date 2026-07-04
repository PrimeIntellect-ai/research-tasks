# test_final_state.py

import os
import subprocess
import pytest

def test_generate_policy_score():
    script_path = "/home/user/generate_policy.py"
    assert os.path.isfile(script_path), f"Agent script not found at {script_path}"

    working_dir = "/home/user"

    # 1. Execute the agent's script to generate policy.json
    try:
        run_script = subprocess.run(
            ["python3", script_path],
            cwd=working_dir,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent script execution failed (exit code {e.returncode}).\nStdout: {e.stdout}\nStderr: {e.stderr}")

    policy_path = os.path.join(working_dir, "policy.json")
    assert os.path.isfile(policy_path), f"Expected policy file not generated at {policy_path}"

    # 2. Run the sec_eval binary on the generated policy.json
    eval_bin = "/app/sec_eval"
    try:
        run_eval = subprocess.run(
            [eval_bin, "policy.json"],
            cwd=working_dir,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"sec_eval execution failed (exit code {e.returncode}).\nStdout: {e.stdout}\nStderr: {e.stderr}")

    # 3. Parse the score and assert threshold
    stdout_str = run_eval.stdout.strip()
    try:
        score = float(stdout_str)
    except ValueError:
        pytest.fail(f"sec_eval output could not be parsed as a float. Output was: {stdout_str!r}")

    threshold = 0.95
    assert score >= threshold, f"Generated policy score {score} is below the required threshold of {threshold}"