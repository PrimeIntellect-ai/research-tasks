# test_final_state.py

import os
import re
import subprocess

def test_solution_file_exists():
    assert os.path.isfile("/home/user/solution.txt"), "/home/user/solution.txt is missing"

def test_solution_token_correct():
    token_path = "/home/user/worker_node/.secret_token"
    solution_path = "/home/user/solution.txt"

    assert os.path.isfile(token_path), f"{token_path} is missing"
    assert os.path.isfile(solution_path), f"{solution_path} is missing"

    with open(token_path, "r") as f:
        expected_token = f.read().strip()

    with open(solution_path, "r") as f:
        solution_content = f.read()

    # Find the token in the solution file
    match = re.search(r"TOKEN:\s*(STUCK_JOB_ID_[a-zA-Z0-9]{16})", solution_content)
    assert match is not None, "Could not find a valid TOKEN line in /home/user/solution.txt"

    actual_token = match.group(1)
    assert actual_token == expected_token, f"Extracted token ({actual_token}) does not match the expected secret token."

def test_processor_fixed_exists():
    assert os.path.isfile("/home/user/worker_node/processor_fixed.py"), "/home/user/worker_node/processor_fixed.py is missing"

def test_processor_fixed_runs_without_deadlock():
    script_path = "/home/user/worker_node/processor_fixed.py"
    assert os.path.isfile(script_path), f"{script_path} is missing"

    try:
        # Run the fixed script with a timeout of 5 seconds
        result = subprocess.run(
            ["python3", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True
        )
        assert result.returncode == 0, f"processor_fixed.py exited with non-zero code {result.returncode}.\nStderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        assert False, "processor_fixed.py timed out after 5 seconds, indicating a deadlock is still present."