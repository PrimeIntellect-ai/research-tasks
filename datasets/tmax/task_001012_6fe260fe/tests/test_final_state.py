# test_final_state.py

import os
import json
import socket
import pytest

BASE_DIR = "/home/user/api_integration"

def test_shared_libraries_exist():
    lib_c = os.path.join(BASE_DIR, "libbackend_c.so")
    lib_cpp = os.path.join(BASE_DIR, "libbackend_cpp.so")

    assert os.path.isfile(lib_c), f"Expected shared library {lib_c} does not exist. Did you compile backend_c.c?"
    assert os.path.isfile(lib_cpp), f"Expected shared library {lib_cpp} does not exist. Did you compile backend_cpp.cpp?"

def test_json_files_exist_and_sorted():
    v1_path = os.path.join(BASE_DIR, "v1_sorted.json")
    v2_path = os.path.join(BASE_DIR, "v2_sorted.json")

    assert os.path.isfile(v1_path), f"{v1_path} does not exist."
    assert os.path.isfile(v2_path), f"{v2_path} does not exist."

    with open(v1_path, 'r') as f1, open(v2_path, 'r') as f2:
        try:
            v1_data = json.load(f1)
            v2_data = json.load(f2)
        except json.JSONDecodeError:
            pytest.fail("One or both of the generated JSON files contain invalid JSON.")

    assert isinstance(v1_data, list), "v1_sorted.json does not contain a JSON array."
    assert isinstance(v2_data, list), "v2_sorted.json does not contain a JSON array."

    # Check if sorted by id
    v1_ids = [item.get('id') for item in v1_data]
    v2_ids = [item.get('id') for item in v2_data]

    assert v1_ids == sorted(v1_ids), "v1_sorted.json is not sorted by 'id' in ascending order."
    assert v2_ids == sorted(v2_ids), "v2_sorted.json is not sorted by 'id' in ascending order."

    # Check if identical in content
    assert v1_data == v2_data, "The parsed JSON contents of v1_sorted.json and v2_sorted.json do not match."

def test_json_files_strictly_identical():
    v1_path = os.path.join(BASE_DIR, "v1_sorted.json")
    v2_path = os.path.join(BASE_DIR, "v2_sorted.json")

    with open(v1_path, 'rb') as f1, open(v2_path, 'rb') as f2:
        assert f1.read() == f2.read(), "v1_sorted.json and v2_sorted.json are not strictly identical byte-for-byte."

def test_diff_output_empty():
    diff_path = os.path.join(BASE_DIR, "diff_output.txt")
    assert os.path.isfile(diff_path), f"{diff_path} does not exist."

    assert os.path.getsize(diff_path) == 0, f"{diff_path} is not empty. The diff command likely found differences."

def test_api_server_terminated():
    # Try to bind to port 5000 to ensure the background API server was terminated
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # If connect succeeds, the server is still running
        s.connect(('127.0.0.1', 5000))
        server_running = True
    except ConnectionRefusedError:
        server_running = False
    finally:
        s.close()

    assert not server_running, "The API server on port 5000 is still running. It was not cleanly terminated."