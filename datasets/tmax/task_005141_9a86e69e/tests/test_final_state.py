# test_final_state.py
import os
import stat
import subprocess
import urllib.request

def test_result_log_contents():
    log_path = '/home/user/result.log'
    assert os.path.isfile(log_path), f"File {log_path} is missing."
    with open(log_path, 'r') as f:
        content = f.read()
    assert "Backend active" in content, f"Expected 'Backend active' in {log_path}, got: {content}"

def test_crontab_configured():
    try:
        output = subprocess.check_output(['crontab', '-l'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    assert "/home/user/start_backend.sh" in output, "crontab does not contain a reference to /home/user/start_backend.sh"

def test_main_go_exists():
    go_path = '/home/user/main.go'
    assert os.path.isfile(go_path), f"File {go_path} is missing."
    with open(go_path, 'r') as f:
        content = f.read()
    assert "package main" in content, f"{go_path} does not appear to be valid Go code."

def test_backend_executable_exists():
    exe_path = '/home/user/backend'
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_start_script_exists_and_executable():
    script_path = '/home/user/start_backend.sh'
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_backend_socket_exists():
    sock_path = '/home/user/backend.sock'
    assert os.path.exists(sock_path), f"Socket {sock_path} is missing."
    mode = os.stat(sock_path).st_mode
    assert stat.S_ISSOCK(mode), f"File {sock_path} is not a socket."

def test_nginx_proxy_working():
    try:
        req = urllib.request.Request("http://127.0.0.1:8888/")
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
            assert "Backend active" in content, "Nginx proxy did not return the expected backend response."
    except Exception as e:
        assert False, f"Failed to connect to Nginx proxy or retrieve backend response: {e}"