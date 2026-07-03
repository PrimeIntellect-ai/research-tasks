# test_final_state.py

import os
import json
import urllib.request
import urllib.error

def test_approved_users_csv():
    path = "/home/user/approved_users.csv"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip().splitlines()

    expected = [
        "bob,bob@example.com",
        "david,david@example.com",
        "eve,eve@example.com"
    ]

    assert content == expected, f"Content of {path} does not match expected output."

def test_cpp_files_exist():
    cpp_path = "/home/user/json_generator.cpp"
    exe_path = "/home/user/json_generator"

    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} does not exist."
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_public_html_json():
    path = "/home/user/public_html/users.json"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} does not contain valid JSON."

    expected = [
        {"username": "bob", "email": "bob@example.com"},
        {"username": "david", "email": "david@example.com"},
        {"username": "eve", "email": "eve@example.com"}
    ]

    assert data == expected, f"JSON content in {path} does not match expected output."

def test_final_output_json():
    path = "/home/user/final_output.json"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} does not contain valid JSON."

    expected = [
        {"username": "bob", "email": "bob@example.com"},
        {"username": "david", "email": "david@example.com"},
        {"username": "eve", "email": "eve@example.com"}
    ]

    assert data == expected, f"JSON content in {path} does not match expected output."

def test_port_forwarding():
    url = "http://127.0.0.1:9090/users.json"
    try:
        req = urllib.request.urlopen(url, timeout=2)
        content = req.read().decode('utf-8')
        data = json.loads(content)
    except urllib.error.URLError:
        assert False, f"Could not connect to {url}. Port forwarding or HTTP server might not be running."
    except json.JSONDecodeError:
        assert False, f"Response from {url} is not valid JSON."

    expected = [
        {"username": "bob", "email": "bob@example.com"},
        {"username": "david", "email": "david@example.com"},
        {"username": "eve", "email": "eve@example.com"}
    ]

    assert data == expected, f"JSON content fetched from {url} does not match expected output."