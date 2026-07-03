# test_final_state.py
import os

def test_parsed_secrets_file():
    path = "/home/user/parsed_secrets.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist. The task requires generating this file."

    with open(path, 'rb') as f:
        content_bytes = f.read()

    try:
        content_str = content_bytes.decode('utf-8')
    except UnicodeDecodeError:
        assert False, f"File {path} is not a valid UTF-8 encoded file."

    lines = [line.strip() for line in content_str.strip().split('\n') if line.strip()]

    expected_lines = [
        "node_A: secret123",
        "node_B: super_secure",
        "node_C: adminPass"
    ]

    assert lines == expected_lines, f"Content of {path} does not match the expected output. Expected: {expected_lines}, Got: {lines}"