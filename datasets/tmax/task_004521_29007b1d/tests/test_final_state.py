# test_final_state.py

import os
import subprocess
import pytest

def test_result_file_exists_and_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} is missing."

    with open(result_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["David", "Eve", "Frank"]
    assert lines == expected, f"Expected {expected} in {result_path}, but got {lines}."

def test_script_fixed_dynamically():
    script_path = "/home/user/get_2nd_degree.py"
    db_path = "/home/user/graph.db"

    assert os.path.isfile(script_path), f"Python script {script_path} is missing."
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    # Test for user_id = 2 (Bob)
    # Bob's 1st degree: David(4), Eve(5)
    # David's friends: Grace(7)
    # Eve's friends: none
    # 2nd degree for Bob: Grace

    try:
        result = subprocess.run(
            ["python3", script_path, db_path, "2"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executing the script failed: {e.stderr}")

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    expected_output = ["Grace"]

    assert output_lines == expected_output, (
        f"The script did not return the correct 2nd degree connections for user_id=2. "
        f"Expected {expected_output}, got {output_lines}."
    )