# test_final_state.py
import os
import json
import subprocess
import time
import urllib.request
import urllib.error

def test_symlinks_and_dirs():
    app_dir = "/home/user/app"
    conf_symlink = os.path.join(app_dir, "conf")
    logs_symlink = os.path.join(app_dir, "logs")
    internal_conf = os.path.join(app_dir, "internal_conf")
    local_logs = os.path.join(app_dir, "local_logs")

    assert os.path.isdir(internal_conf), f"Target directory {internal_conf} does not exist."
    assert os.path.isdir(local_logs), f"Target directory {local_logs} does not exist."

    assert os.path.islink(conf_symlink), f"{conf_symlink} is not a symlink."
    assert os.readlink(conf_symlink) == internal_conf, f"{conf_symlink} does not point to {internal_conf}."

    assert os.path.islink(logs_symlink), f"{logs_symlink} is not a symlink."
    assert os.readlink(logs_symlink) == local_logs, f"{logs_symlink} does not point to {local_logs}."

def test_backends_json():
    backends_path = "/home/user/app/conf/backends.json"
    assert os.path.isfile(backends_path), f"Configuration file {backends_path} does not exist."

    with open(backends_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{backends_path} does not contain valid JSON."

    expected = ["http://127.0.0.1:8081", "http://127.0.0.1:8082"]
    assert data == expected, f"Contents of {backends_path} do not match expected array."

def test_ci_cd_verify():
    script_path = "/home/user/ci_cd_verify.sh"
    status_file = "/home/user/deploy_status.txt"

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Remove status file if it exists to ensure a fresh run
    if os.path.exists(status_file):
        os.remove(status_file)

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed with exit code {result.returncode}. Output: {result.stderr}"

    assert os.path.isfile(status_file), f"{status_file} was not created by the script."
    with open(status_file, 'r') as f:
        status = f.read().strip()

    assert status == "PIPELINE_SUCCESS", f"Expected PIPELINE_SUCCESS in {status_file}, got '{status}'."

def test_proxy_js():
    proxy_script = "/home/user/app/proxy.js"
    pid_file = "/home/user/app/logs/proxy.pid"

    assert os.path.isfile(proxy_script), f"Proxy script {proxy_script} does not exist."

    if os.path.exists(pid_file):
        os.remove(pid_file)

    # Start the proxy script
    process = subprocess.Popen(["node", proxy_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Give it a moment to start
        time.sleep(2)

        # Check if process is still running
        assert process.poll() is None, f"Proxy script exited prematurely. Error: {process.stderr.read().decode()}"

        # Test HTTP response
        try:
            req = urllib.request.Request("http://127.0.0.1:8080")
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status == 200, f"Expected HTTP 200, got {response.status}"
                body = response.read().decode('utf-8').strip()
                assert body == "PROXY_ACTIVE", f"Expected response 'PROXY_ACTIVE', got '{body}'"
        except urllib.error.URLError as e:
            assert False, f"Failed to connect to proxy server: {e}"

        # Check PID file
        assert os.path.isfile(pid_file), f"PID file {pid_file} was not created."
        with open(pid_file, 'r') as f:
            pid_str = f.read().strip()
            assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid numeric PID."

    finally:
        # Cleanup
        process.terminate()
        process.wait(timeout=5)