# test_final_state.py

import os
import json
import time
import subprocess
import urllib.request
import pytest

def get_running_pids(script_name):
    """Return a list of PIDs running the given script name, ignoring grep."""
    pids = []
    try:
        output = subprocess.check_output(['ps', '-eo', 'pid,args']).decode('utf-8')
        for line in output.strip().split('\n'):
            if script_name in line and 'grep' not in line and 'vim' not in line and 'nano' not in line:
                pid = int(line.split()[0])
                pids.append(pid)
    except Exception:
        pass
    return pids

def test_scripts_exist_and_executable():
    scripts = [
        '/home/user/proxy.py',
        '/home/user/supervisor.py',
        '/home/user/deploy.py'
    ]
    for script in scripts:
        assert os.path.isfile(script), f"{script} does not exist."
        assert os.access(script, os.X_OK), f"{script} is not executable."

def test_metrics_log():
    log_path = '/home/user/metrics.log'
    assert os.path.isfile(log_path), f"{log_path} does not exist."
    with open(log_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{log_path} does not contain valid JSON.")

    assert data.get('dashboard') == 'up', "Dashboard status in metrics.log is not 'up'."
    assert data.get('data', {}).get('status') == 'ok', "Data status in metrics.log is not 'ok'."
    assert data.get('data', {}).get('metric') == 42, "Metric value in metrics.log is incorrect."

def test_dashboard_endpoint_live():
    try:
        req = urllib.request.Request("http://127.0.0.1:8082/")
        with urllib.request.urlopen(req, timeout=3) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode())
            assert data.get('dashboard') == 'up', "Live dashboard status is not 'up'. Proxy may not be forwarding correctly."
    except Exception as e:
        pytest.fail(f"Failed to contact dashboard endpoint: {e}")

def test_supervisor_and_proxy_running():
    supervisor_pids = get_running_pids('supervisor.py')
    assert len(supervisor_pids) > 0, "supervisor.py is not running."

    proxy_pids = get_running_pids('proxy.py')
    assert len(proxy_pids) > 0, "proxy.py is not running."

def test_supervisor_restarts_proxy():
    proxy_pids_before = get_running_pids('proxy.py')
    assert len(proxy_pids_before) > 0, "proxy.py is not running initially."

    # Kill proxy processes
    for pid in proxy_pids_before:
        try:
            os.kill(pid, 9)
        except OSError:
            pass

    # Give the supervisor time to detect and restart the proxy
    time.sleep(3)

    proxy_pids_after = get_running_pids('proxy.py')
    assert len(proxy_pids_after) > 0, "proxy.py was not restarted by supervisor after being killed."
    assert set(proxy_pids_before).isdisjoint(set(proxy_pids_after)), "proxy.py has the same PID, so it was not restarted."

def test_deploy_idempotent():
    # Run deploy.py again
    try:
        subprocess.run(['python3', '/home/user/deploy.py'], check=True, timeout=5)
    except subprocess.TimeoutExpired:
        pytest.fail("deploy.py did not exit. It must run the supervisor in the background and exit.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"deploy.py failed when run a second time: {e}")

    time.sleep(1)

    supervisor_pids = get_running_pids('supervisor.py')
    # Remove any deploy.py processes that might have matched if they hung
    supervisor_pids = [pid for pid in supervisor_pids if pid not in get_running_pids('deploy.py')]

    assert len(supervisor_pids) == 1, f"Expected exactly 1 supervisor.py running after redeploy, found {len(supervisor_pids)}."