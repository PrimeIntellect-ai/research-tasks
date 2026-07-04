# test_final_state.py

import os
import subprocess

def test_verification_file():
    verification_path = "/home/user/verification.txt"
    assert os.path.isfile(verification_path), f"Verification file not found at {verification_path}. Did you run curl and save the output?"

    with open(verification_path, "r") as f:
        content = f.read().strip()

    expected_content = "<h1>Welcome to the secure app</h1>"
    assert expected_content in content, f"Verification file does not contain the expected text. Found: {content}"

def test_symlink_validity():
    symlink_path = "/home/user/containers/app1/www"
    assert os.path.islink(symlink_path) or os.path.isdir(symlink_path), f"Expected {symlink_path} to be a valid directory or symlink."

    # Check if it resolves to the correct directory containing index.html
    index_path = os.path.join(symlink_path, "index.html")
    assert os.path.isfile(index_path), f"Symlink {symlink_path} does not correctly point to a directory containing index.html."

    with open(index_path, "r") as f:
        content = f.read().strip()
    assert content == "<h1>Welcome to the secure app</h1>", "The index.html served by the symlink does not match the static files content."

def test_certificates_exist():
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file not found at {cert_path}."
    assert os.path.isfile(key_path), f"Private key file not found at {key_path}."

def test_server_running():
    pid_file = "/home/user/containers/app1/server.pid"
    assert os.path.isfile(pid_file), f"PID file not found at {pid_file}. Did the manager script start the server?"

    with open(pid_file, "r") as f:
        pid = f.read().strip()

    assert pid.isdigit(), f"Invalid PID found in {pid_file}: {pid}"

    # Check if the process is actually running
    try:
        os.kill(int(pid), 0)
    except OSError:
        assert False, f"Process with PID {pid} is not running. The server might have crashed."