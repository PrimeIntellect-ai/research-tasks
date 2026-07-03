# test_final_state.py

import os
import urllib.request
import urllib.error

def test_post_receive_hook():
    hook_path = "/home/user/app.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook file {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Hook file {hook_path} is not executable."

    with open(hook_path, "r") as f:
        first_line = f.readline().strip()

    assert first_line.startswith("#!") and "python" in first_line.lower(), \
        f"Hook file {hook_path} does not have a valid Python shebang. Found: {first_line}"

def test_deploy_server_py():
    deploy_file = "/home/user/deploy/server.py"
    assert os.path.isfile(deploy_file), f"Deployed server file {deploy_file} does not exist. Did the hook extract the code?"

def test_deploy_log():
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "Deployment successful" in content, f"Log file {log_path} does not contain 'Deployment successful'."

def test_server_running():
    pid_file = "/home/user/deploy/server.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer PID. Found: '{pid_str}'"

    pid = int(pid_str)
    proc_cmdline = f"/proc/{pid}/cmdline"
    assert os.path.isfile(proc_cmdline), f"Process with PID {pid} is not running."

    with open(proc_cmdline, "r") as f:
        cmdline = f.read().replace('\x00', ' ')

    assert "python" in cmdline.lower() and "server.py" in cmdline, \
        f"Process {pid} is running, but does not appear to be the Python server. Cmdline: {cmdline}"

def test_server_responds():
    url = "http://127.0.0.1:8080"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to the server at {url}: {e}"