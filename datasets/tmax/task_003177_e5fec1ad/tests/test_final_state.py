# test_final_state.py

import os
import socket
import urllib.request
import urllib.error
import json
import subprocess

def test_backup_exists_and_content():
    backup_file = "/home/user/backup/collector.c.bak"
    assert os.path.isfile(backup_file), f"Backup file {backup_file} does not exist."
    with open(backup_file, 'r') as f:
        content = f.read()
    assert '"./metrics.json"' in content, f"Original path './metrics.json' not found in backup file {backup_file}."

def test_collector_c_updated_and_compiled():
    c_file = "/home/user/src/collector.c"
    assert os.path.isfile(c_file), f"File {c_file} does not exist."
    with open(c_file, 'r') as f:
        content = f.read()
    assert '"/home/user/dashboard/metrics.json"' in content, f"Updated path '/home/user/dashboard/metrics.json' not found in {c_file}."

    binary_file = "/home/user/bin/collector"
    assert os.path.isfile(binary_file), f"Binary {binary_file} does not exist."
    assert os.access(binary_file, os.X_OK), f"Binary {binary_file} is not executable."

    # Check if binary was compiled after the source was updated
    c_mtime = os.path.getmtime(c_file)
    bin_mtime = os.path.getmtime(binary_file)
    assert bin_mtime >= c_mtime, f"Binary {binary_file} is older than source {c_file}. Did you recompile?"

def test_metrics_json_generated():
    metrics_file = "/home/user/dashboard/metrics.json"
    assert os.path.isfile(metrics_file), f"Metrics file {metrics_file} does not exist. Did you run the recompiled binary?"
    with open(metrics_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Metrics file {metrics_file} does not contain valid JSON."
    assert data.get("status") == "ok", "Metrics JSON missing 'status': 'ok'."
    assert data.get("active_users") == 42, "Metrics JSON missing 'active_users': 42."

def test_socat_proxy_running():
    pid_file = "/home/user/proxy.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."
    with open(pid_file, 'r') as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer."

    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} is not running."

    # Check if socat is listening on 9090
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('127.0.0.1', 9090))
    sock.close()
    assert result == 0, "Nothing is listening on 127.0.0.1:9090. Is socat running correctly?"

def test_proxy_forwarding_works():
    # Test if we can fetch metrics.json via the proxy
    try:
        req = urllib.request.urlopen("http://127.0.0.1:9090/metrics.json", timeout=2)
        content = req.read().decode('utf-8')
        data = json.loads(content)
        assert data.get("active_users") == 42, "Fetched metrics JSON via proxy is incorrect."
    except urllib.error.URLError as e:
        assert False, f"Failed to fetch metrics via proxy on port 9090: {e}"
    except json.JSONDecodeError:
        assert False, "Data fetched via proxy is not valid JSON."