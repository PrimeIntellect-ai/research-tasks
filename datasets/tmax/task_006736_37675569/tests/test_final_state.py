# test_final_state.py
import os
import subprocess

def test_api_parser_sh_exists_and_executable():
    path = "/home/user/api_parser.sh"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_test_runner_sh_exists():
    path = "/home/user/test_runner.sh"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_test_results_log_content():
    path = "/home/user/test_results.log"
    assert os.path.exists(path), f"File {path} does not exist. Did you run test_runner.sh?"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        '{"id": "99", "data": "Bash is fun"}',
        '{"id": "42", "data": "Only Payload"}',
        '{"id": "7", "data": ""}'
    ]

    assert len(lines) == 3, f"Expected 3 lines in {path}, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."

def test_api_parser_sh_functionality():
    # Test the bash script directly to ensure it actually works and wasn't just hardcoded
    path = "/home/user/api_parser.sh"
    test_url = "http://example.com/api?payload=SGVsbG8gV29ybGQ=&id=123"

    try:
        result = subprocess.run([path, test_url], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        expected_output = '{"id": "123", "data": "Hello World"}'
        assert output == expected_output, f"api_parser.sh output mismatch. Expected '{expected_output}', got '{output}'."
    except subprocess.CalledProcessError as e:
        assert False, f"api_parser.sh failed to execute: {e.stderr}"