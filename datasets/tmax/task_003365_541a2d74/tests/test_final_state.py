# test_final_state.py

import os
import json
import pytest

def test_cert_flag_content():
    path = "/home/user/cert_flag.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The SSL certificate flag was not saved."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "FLAG{C3rt_0rganizati0n_L3ak}"
    assert content == expected, f"Content of {path} is incorrect. Expected '{expected}', got '{content}'."

def test_auth_flag_content():
    path = "/home/user/auth_flag.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The HTTP basic auth flag was not saved."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "FLAG{Brut3_F0rc3_M4st3r}"
    assert content == expected, f"Content of {path} is incorrect. Expected '{expected}', got '{content}'."

def test_pentest_summary_json():
    path = "/home/user/pentest_summary.json"
    assert os.path.isfile(path), f"File {path} does not exist. The pentest summary report was not created."

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {path} is not a valid JSON file.")

    assert isinstance(data, dict), f"JSON content in {path} must be a dictionary."

    assert "https_port" in data, "Key 'https_port' is missing from pentest_summary.json."
    assert data["https_port"] == 8443, f"Incorrect https_port. Expected 8443, got {data['https_port']}."

    assert "http_port" in data, "Key 'http_port' is missing from pentest_summary.json."
    assert data["http_port"] == 8080, f"Incorrect http_port. Expected 8080, got {data['http_port']}."

    assert "cracked_password" in data, "Key 'cracked_password' is missing from pentest_summary.json."
    assert data["cracked_password"] == "hunter2", f"Incorrect cracked_password. Expected 'hunter2', got {data['cracked_password']}."