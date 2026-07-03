# test_final_state.py
import os
import subprocess
import pty
import time
import requests

def run_ssh_with_password(user, password, port=2222):
    pid, fd = pty.fork()
    if pid == 0:
        # Child process
        os.execvp("ssh", [
            "ssh", 
            "-o", "StrictHostKeyChecking=no", 
            "-o", "UserKnownHostsFile=/dev/null", 
            "-o", "PubkeyAuthentication=no", 
            "-o", "PreferredAuthentications=password",
            "-p", str(port), 
            f"{user}@127.0.0.1"
        ])
    else:
        # Parent process
        output = b""
        password_sent = False
        while True:
            try:
                data = os.read(fd, 1024)
            except OSError:
                break
            if not data:
                break
            output += data
            if b"password:" in data.lower() and not password_sent:
                os.write(fd, password.encode() + b"\n")
                password_sent = True

        _, status = os.waitpid(pid, 0)
        exit_code = os.waitstatus_to_exitcode(status) if hasattr(os, 'waitstatus_to_exitcode') else (status >> 8)
        return exit_code, output.decode(errors='ignore')

def test_http_health_check():
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to HTTP API on port 8080: {e}"

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert response.text.strip() == "OK", f"Expected body 'OK', got '{response.text}'"

def test_ssh_pubkey_auth_fails():
    # Attempt SSH with pubkey auth only
    result = subprocess.run([
        "ssh", 
        "-o", "StrictHostKeyChecking=no", 
        "-o", "UserKnownHostsFile=/dev/null", 
        "-o", "PasswordAuthentication=no", 
        "-o", "PreferredAuthentications=publickey",
        "-p", "2222", 
        "sysadmin@127.0.0.1"
    ], capture_output=True, text=True)

    assert result.returncode != 0, "Public key authentication should have failed, but it succeeded."
    assert "Permission denied" in result.stderr or "Connection closed" in result.stderr, "Expected permission denied or connection closed for pubkey auth."

def test_ssh_wrong_password_fails():
    exit_code, output = run_ssh_with_password("sysadmin", "wrongpass")
    assert exit_code != 0, "Authentication with wrong password should have failed."
    assert "Welcome sysadmin" not in output, "Should not see welcome message with wrong password."

def test_ssh_correct_password_succeeds():
    exit_code, output = run_ssh_with_password("sysadmin", "legacy_p4ss")
    assert "Welcome sysadmin" in output, f"Expected 'Welcome sysadmin' in output, got: {output}"