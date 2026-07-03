# test_final_state.py

import os
import json
import socket
import pytest

def test_diff_txt_empty():
    path = "/home/user/diff.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The task requires running the diff command and saving to this file."
    assert os.path.getsize(path) == 0, f"File {path} is not empty. This means the outputs from the Python 2 script and the Rust service did not match."

def test_rust_min_json_content():
    path = "/home/user/rust_min.json"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    expected = [
        {"id": "B1", "timestamp": 1620000100, "value": "qux"},
        {"id": "A2", "timestamp": 1620000050, "value": "bar"},
        {"id": "A1", "timestamp": 1620000000, "value": "foo"},
        {"id": "A3", "timestamp": 1619999900, "value": "baz"},
        {"id": "B2", "timestamp": 1619999800, "value": "quux"}
    ]

    assert data == expected, f"The content of {path} does not match the expected sorted data."

def test_nginx_running():
    try:
        with socket.create_connection(('127.0.0.1', 8080), timeout=2):
            pass
    except OSError:
        pytest.fail("Nginx does not appear to be running or bound to 127.0.0.1:8080. Ensure it was started and left running.")

def test_rust_server_running():
    try:
        with socket.create_connection(('127.0.0.1', 3000), timeout=2):
            pass
    except OSError:
        pytest.fail("Rust service does not appear to be running or bound to 127.0.0.1:3000. Ensure it was started in the background and left running.")