# test_final_state.py
import os
import stat
import json
import urllib.request
import ssl
import subprocess
import pytest

def test_mailing_lists_permissions():
    directory = "/home/user/mailing_lists"
    assert os.path.isdir(directory), f"Directory {directory} does not exist."

    files = [f for f in os.listdir(directory) if f.endswith(".list_config")]
    assert len(files) == 4, f"Expected 4 .list_config files, found {len(files)}."

    for filename in files:
        filepath = os.path.join(directory, filename)
        st = os.stat(filepath)
        perms = stat.S_IMODE(st.st_mode)
        assert perms == 0o600, f"File {filepath} has incorrect permissions: {oct(perms)}. Expected 0o600."

def test_status_json_contents():
    filepath = "/home/user/status.json"
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{filepath} does not contain valid JSON.")

    expected_keys = {"alice", "bob", "charlie", "diana"}
    assert set(data.keys()) == expected_keys, f"Expected keys {expected_keys}, found {set(data.keys())}."
    assert data["alice"] == "alice@example.com", "Incorrect email for alice."
    assert data["bob"] == "bob@example.com", "Incorrect email for bob."
    assert data["charlie"] == "charlie@example.com", "Incorrect email for charlie."
    assert data["diana"] == "diana@example.com", "Incorrect email for diana."

def test_https_server_response():
    url = "https://localhost:8443/status.json"

    # Create an unverified context to bypass self-signed certificate validation
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}."
            content = response.read().decode('utf-8')
            data = json.loads(content)
            expected_keys = {"alice", "bob", "charlie", "diana"}
            assert set(data.keys()) == expected_keys, f"Server returned incorrect JSON keys: {set(data.keys())}."
    except Exception as e:
        pytest.fail(f"Failed to fetch from HTTPS server: {e}")

def test_processes_running():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run ps command: {e}")

    assert "monitor.py" in output, "monitor.py is not running in the background."
    assert "server.py" in output, "server.py is not running in the background."