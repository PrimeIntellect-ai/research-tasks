# test_final_state.py

import os
import stat
import json
import urllib.request
import urllib.error
import subprocess

def test_config_and_secret_files():
    config_path = '/home/user/service/config.json'
    secret_path = '/home/user/service/secret.key'

    assert os.path.isfile(config_path), f"{config_path} does not exist."
    assert os.path.isfile(secret_path), f"{secret_path} does not exist."

    # Check config.json permissions and content
    config_stat = os.stat(config_path)
    assert stat.S_IMODE(config_stat.st_mode) == 0o600, f"{config_path} permissions are not exactly 0600."

    with open(config_path, 'r') as f:
        try:
            config_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{config_path} does not contain valid JSON."

    expected_config = {"bind_host": "127.0.0.1", "bind_port": 5050, "log_file": "/home/user/service/access.log"}
    assert config_data == expected_config, f"{config_path} content does not match the expected JSON."

    # Check secret.key permissions and content
    secret_stat = os.stat(secret_path)
    assert stat.S_IMODE(secret_stat.st_mode) == 0o400, f"{secret_path} permissions are not exactly 0400."

    with open(secret_path, 'rb') as f:
        secret_content = f.read()
    assert secret_content == b'METRICS_TOKEN_xyz123', f"{secret_path} content does not match the exact expected string."

def test_primary_service_health():
    url = 'http://127.0.0.1:5050/health'
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200 from {url}, got {response.status}."
            body = response.read().decode('utf-8')
            assert body == 'OK', f"Expected body 'OK' from {url}, got '{body}'."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to primary service at {url}: {e}"

def test_primary_service_metrics_unauthorized():
    url = 'http://127.0.0.1:5050/metrics'
    req = urllib.request.Request(url)
    try:
        urllib.request.urlopen(req, timeout=2)
        assert False, f"Expected HTTP 403 Forbidden from {url} when no token is provided, but request succeeded."
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected HTTP 403 from {url} without token, got {e.code}."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to primary service at {url}: {e}"

def test_primary_service_metrics_authorized():
    url = 'http://127.0.0.1:5050/metrics'
    req = urllib.request.Request(url)
    req.add_header('X-Auth-Token', 'METRICS_TOKEN_xyz123')
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200 from {url} with valid token, got {response.status}."
            body = response.read().decode('utf-8')
            assert body == 'SECURE_METRICS_DATA', f"Expected body 'SECURE_METRICS_DATA' from {url}, got '{body}'."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to primary service at {url} with token: {e}"

def test_firewall_proxy_allowed():
    url = 'http://127.0.0.1:6060/health'
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200 from proxy at {url}, got {response.status}."
            body = response.read().decode('utf-8')
            assert body == 'OK', f"Expected body 'OK' from proxy at {url}, got '{body}'."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to firewall proxy at {url}: {e}"

def test_firewall_proxy_code_for_acls():
    proxy_script = '/home/user/service/firewall_proxy.py'
    assert os.path.isfile(proxy_script), f"{proxy_script} does not exist."
    with open(proxy_script, 'r') as f:
        content = f.read()
    assert '10.0.0.55' in content, f"Expected to find IP '10.0.0.55' in {proxy_script} for ACL checks."
    assert '127.0.0.1' in content, f"Expected to find IP '127.0.0.1' in {proxy_script} for ACL checks."

def test_monitor_script():
    monitor_script = '/home/user/service/monitor.sh'
    log_file = '/home/user/service/monitor.log'

    assert os.path.isfile(monitor_script), f"{monitor_script} does not exist."
    assert os.access(monitor_script, os.X_OK), f"{monitor_script} is not executable."

    if os.path.exists(log_file):
        os.remove(log_file)

    try:
        subprocess.run([monitor_script], check=True, timeout=5)
    except subprocess.CalledProcessError as e:
        assert False, f"Execution of {monitor_script} failed with exit code {e.returncode}."
    except subprocess.TimeoutExpired:
        assert False, f"Execution of {monitor_script} timed out."

    assert os.path.isfile(log_file), f"{log_file} was not created by the monitor script."

    with open(log_file, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, f"{log_file} is empty."
    last_line = lines[-1].strip()
    assert last_line == '[OK] Service is healthy', f"Expected log entry '[OK] Service is healthy', got '{last_line}'."