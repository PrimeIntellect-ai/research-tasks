# test_final_state.py
import os

def test_agg_results():
    user_file = '/home/user/agg_results.csv'
    expected_file = '/home/user/expected_agg_results.csv'

    assert os.path.exists(user_file), f"Expected file {user_file} does not exist."

    with open(user_file, 'r') as f:
        user_content = f.read().strip().splitlines()

    with open(expected_file, 'r') as f:
        expected_content = f.read().strip().splitlines()

    assert user_content == expected_content, f"Content of {user_file} does not match expected output."

def test_model_metrics():
    user_file = '/home/user/model_metrics.txt'
    expected_file = '/home/user/expected_model_metrics.txt'

    assert os.path.exists(user_file), f"Expected file {user_file} does not exist."

    with open(user_file, 'r') as f:
        user_content = f.read().strip()

    with open(expected_file, 'r') as f:
        expected_content = f.read().strip()

    assert user_content == expected_content, f"Content of {user_file} does not match expected output. Expected '{expected_content}', got '{user_content}'."