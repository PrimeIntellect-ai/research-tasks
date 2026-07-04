# test_final_state.py
import os
import time
import subprocess
import urllib.request
import urllib.error

def test_directories_exist():
    assert os.path.isdir('/home/user/app_data'), "Directory /home/user/app_data does not exist"
    assert os.path.isdir('/home/user/supervisor_logs'), "Directory /home/user/supervisor_logs does not exist"

def test_processes_running():
    ps_output = subprocess.check_output(['ps', 'x']).decode()
    assert 'lb.py' in ps_output, "Load balancer script (lb.py) is not running"
    assert 'monitor.py' in ps_output, "Monitor script (monitor.py) is not running"
    assert 'backend.py' in ps_output, "Backend scripts are not running"

def test_load_balancer_and_backends():
    ports_hit = set()
    for _ in range(6):
        req = urllib.request.Request('http://127.0.0.1:8080/upload', data=b"testdata", method='POST')
        try:
            resp = urllib.request.urlopen(req, timeout=2)
            body = resp.read().decode().strip()
            assert body.startswith("OK from "), f"Unexpected response body: {body}"
            ports_hit.add(body)
        except Exception as e:
            assert False, f"Load balancer request failed: {e}"

    assert len(ports_hit) == 3, f"Load balancer did not hit all 3 backends. Hit: {ports_hit}"

def test_storage_monitor():
    dummy_path = '/home/user/app_data/backend_9999.dat'
    # Create a dummy file larger than 1MB
    with open(dummy_path, 'wb') as f:
        f.write(b'0' * (1024 * 1024 + 10))

    # Give the monitor time to detect and delete
    time.sleep(4)

    assert not os.path.exists(dummy_path), "Monitor script did not delete the oversized file"

    assert os.path.exists('/home/user/alert.log'), "Alert log (/home/user/alert.log) was not created"
    with open('/home/user/alert.log', 'r') as f:
        log_content = f.read()
        assert "ALERT: Quota exceeded. Deleted backend_9999.dat" in log_content, "Alert log format incorrect or missing entry"

def test_supervisor_restart_policy():
    # Find the PID of the load balancer
    lb_pid_cmd = "ps x | grep '[l]b.py' | awk '{print $1}'"
    try:
        lb_pid = subprocess.check_output(lb_pid_cmd, shell=True).decode().strip()
    except subprocess.CalledProcessError:
        lb_pid = ""

    assert lb_pid != "", "Could not find PID for lb.py to test restart policy"

    # Kill the load balancer
    subprocess.check_call(['kill', '-9', lb_pid])

    # Wait for supervisor to restart it
    time.sleep(3)

    # Check if a new lb.py is running
    try:
        new_lb_pid = subprocess.check_output(lb_pid_cmd, shell=True).decode().strip()
    except subprocess.CalledProcessError:
        new_lb_pid = ""

    assert new_lb_pid != "", "lb.py was not restarted by supervisor"
    assert new_lb_pid != lb_pid, "lb.py PID did not change, kill might have failed"