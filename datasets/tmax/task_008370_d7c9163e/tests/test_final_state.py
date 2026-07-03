# test_final_state.py

import os
import ssl
import urllib.request
import subprocess

def test_tls_certificates():
    assert os.path.isfile("/home/user/tls/cert.pem"), "TLS certificate /home/user/tls/cert.pem is missing"
    assert os.path.isfile("/home/user/tls/key.pem"), "TLS private key /home/user/tls/key.pem is missing"

def test_git_repo_and_hook():
    assert os.path.isdir("/home/user/monitor.git"), "Git bare repository /home/user/monitor.git is missing"
    hook_path = "/home/user/monitor.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} is missing"
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable"

def test_deployed_files():
    assert os.path.isdir("/home/user/app"), "Deployment directory /home/user/app is missing"
    assert os.path.isfile("/home/user/app/server.py"), "server.py is missing in /home/user/app"
    assert os.path.isfile("/home/user/app/deploy_success.txt"), "deploy_success.txt is missing in /home/user/app"
    assert os.path.isfile("/home/user/app/server.pid"), "server.pid is missing in /home/user/app"

def test_web_server_listening():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://127.0.0.1:8443/")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except Exception as e:
        assert False, f"Failed to connect to the HTTPS server on 127.0.0.1:8443: {e}"

def test_c_program_compilation():
    assert os.path.isfile("/home/user/checker.c"), "C source file /home/user/checker.c is missing"
    assert os.path.isfile("/home/user/checker"), "Compiled C program /home/user/checker is missing"
    assert os.access("/home/user/checker", os.X_OK), "Compiled C program /home/user/checker is not executable"

def test_log_file_content():
    log_path = "/home/user/system_status.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing"
    with open(log_path, "r") as f:
        content = f.read()
    assert "SYSTEM: OK" in content, f"'SYSTEM: OK' not found in {log_path}"

def test_c_program_behavior_dynamically():
    checker_path = "/home/user/checker"
    log_path = "/home/user/system_status.log"
    deploy_file = "/home/user/app/deploy_success.txt"

    # Clear log file
    if os.path.exists(log_path):
        os.remove(log_path)

    # Run checker with everything OK
    subprocess.run([checker_path], check=True)
    assert os.path.isfile(log_path), f"Checker did not create {log_path}"
    with open(log_path, "r") as f:
        content = f.read()
    assert "SYSTEM: OK" in content, "Checker did not log 'SYSTEM: OK' when everything is fine"

    # Remove deploy_success.txt to trigger failure
    os.remove(deploy_file)
    try:
        subprocess.run([checker_path], check=True)
        with open(log_path, "r") as f:
            content = f.read()
        assert "SYSTEM: FAIL" in content, "Checker did not log 'SYSTEM: FAIL' when deploy_success.txt is missing"
    finally:
        # Restore the file
        open(deploy_file, 'w').close()