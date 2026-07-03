# test_final_state.py
import os
import re
import subprocess
import pytest
import time

def test_bashrc_env_var():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist"

    with open(bashrc_path, 'r') as f:
        content = f.read()

    # Look for export DEPLOY_ENV=production, allowing optional quotes
    match = re.search(r'export\s+DEPLOY_ENV=["\']?production["\']?', content)
    assert match is not None, "DEPLOY_ENV=production is not exported in /home/user/.bashrc"

def test_cron_job():
    try:
        result = subprocess.run(['crontab', '-l', '-u', 'user'], capture_output=True, text=True)
        crontab_content = result.stdout
    except FileNotFoundError:
        # Fallback if running directly as user without specifying -u
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        crontab_content = result.stdout

    # Look for 5 minute intervals and orchestrator.py
    cron_pattern = r'(?:\*/5|0,5,10,15,20,25,30,35,40,45,50,55)\s+\*\s+\*\s+\*\s+\*.*python3\s+/home/user/orchestrator\.py'
    match = re.search(cron_pattern, crontab_content)
    assert match is not None, "Cron job for orchestrator.py every 5 minutes is missing or incorrect"

def test_orchestrator_executable():
    orch_path = "/home/user/orchestrator.py"
    assert os.path.isfile(orch_path), f"{orch_path} does not exist"
    assert os.access(orch_path, os.X_OK), f"{orch_path} is not executable"

def test_orchestrator_logic():
    orch_path = "/home/user/orchestrator.py"
    pid_file = "/home/user/run/services.pid"

    # Stop existing processes and remove pid file for a clean test
    subprocess.run(['pkill', '-f', '/home/user/services/'], stderr=subprocess.DEVNULL)
    if os.path.exists(pid_file):
        os.remove(pid_file)

    # Test 1: Silent failure when DEPLOY_ENV != production
    env = os.environ.copy()
    env["DEPLOY_ENV"] = "staging"
    result = subprocess.run(['/usr/bin/python3', orch_path], env=env, capture_output=True)
    assert result.returncode == 0, "Orchestrator should exit with 0 when DEPLOY_ENV != production"
    assert not os.path.exists(pid_file), "Orchestrator should not do anything when DEPLOY_ENV != production"

    # Test 2: Successful execution
    env["DEPLOY_ENV"] = "production"
    result = subprocess.run(['/usr/bin/python3', orch_path], env=env, capture_output=True)
    assert result.returncode == 0, "Orchestrator failed to run successfully"

    # Allow a brief moment for processes to start and write to pid file
    time.sleep(1)

    assert os.path.isfile(pid_file), f"PID file {pid_file} was not created"

    with open(pid_file, 'r') as f:
        content = f.read().strip().split('\n')

    pids = {}
    for line in content:
        if ':' in line:
            name, pid = line.split(':', 1)
            pids[name] = int(pid)

    assert 'alpha' in pids, "alpha service not found in services.pid"
    assert 'beta' in pids, "beta service not found in services.pid"

    # Verify processes are running
    for name, pid in pids.items():
        try:
            os.kill(pid, 0)
        except OSError:
            pytest.fail(f"Service {name} with PID {pid} is not actually running")