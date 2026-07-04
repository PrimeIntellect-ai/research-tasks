# test_final_state.py
import os
import subprocess
import pytest

def test_bad_commit_hash():
    user_hash_path = '/home/user/bad_commit_hash.txt'
    expected_hash_path = '/tmp/expected_bad_commit.txt'

    assert os.path.isfile(user_hash_path), f"File {user_hash_path} does not exist."
    assert os.path.isfile(expected_hash_path), f"Truth file {expected_hash_path} does not exist."

    with open(user_hash_path, 'r') as f:
        user_hash = f.read().strip()

    with open(expected_hash_path, 'r') as f:
        expected_hash = f.read().strip()

    assert user_hash == expected_hash, f"Expected bad commit hash '{expected_hash}', but got '{user_hash}'."

def test_final_output():
    output_path = '/home/user/final_output.txt'

    assert os.path.isfile(output_path), f"File {output_path} does not exist."

    with open(output_path, 'r') as f:
        output_content = f.read().strip()

    expected_content = "Total: 673.74"
    assert output_content == expected_content, f"Expected final output to be '{expected_content}', but got '{output_content}'."

def test_parser_py_execution():
    repo_dir = '/home/user/financial_parser'
    script_path = os.path.join(repo_dir, 'parser.py')
    records_path = os.path.join(repo_dir, 'records.txt')

    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    assert os.path.isfile(records_path), f"File {records_path} does not exist."

    result = subprocess.run(
        ['python3', 'parser.py', 'records.txt'],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script crashed with error:\n{result.stderr}"

    output = result.stdout.strip()
    expected_output = "Total: 673.74"

    assert output == expected_output, f"Expected script output to be '{expected_output}', but got '{output}'."