# test_final_state.py
import os
import json
import subprocess
import time
import re
import pytest

APP_DIR = "/home/user/app"
SUPERVISOR_SCRIPT = os.path.join(APP_DIR, "supervisor.sh")
DEPLOY_CHECK_SCRIPT = os.path.join(APP_DIR, "deploy_check.py")
DIAGNOSTIC_JSON = os.path.join(APP_DIR, "diagnostic.json")
RESTARTS_LOG = os.path.join(APP_DIR, "restarts.log")

def test_scripts_exist_and_executable():
    assert os.path.exists(SUPERVISOR_SCRIPT), f"{SUPERVISOR_SCRIPT} does not exist."
    assert os.access(SUPERVISOR_SCRIPT, os.X_OK), f"{SUPERVISOR_SCRIPT} is not executable."

    assert os.path.exists(DEPLOY_CHECK_SCRIPT), f"{DEPLOY_CHECK_SCRIPT} does not exist."
    assert os.access(DEPLOY_CHECK_SCRIPT, os.X_OK), f"{DEPLOY_CHECK_SCRIPT} is not executable."

def test_execution_and_output():
    # Ensure no lingering processes from student's manual testing
    subprocess.run(["pkill", "-f", "supervisor.sh"], capture_output=True)
    subprocess.run(["pkill", "-f", "server.py"], capture_output=True)

    # Clean up old files to ensure we are testing the script's actual output
    if os.path.exists(DIAGNOSTIC_JSON):
        os.remove(DIAGNOSTIC_JSON)
    if os.path.exists(RESTARTS_LOG):
        os.remove(RESTARTS_LOG)

    # Start supervisor
    supervisor_proc = subprocess.Popen(
        [SUPERVISOR_SCRIPT], 
        cwd=APP_DIR, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )

    try:
        # Give the supervisor time to start the server
        time.sleep(2)

        # Run deploy_check.py
        check_proc = subprocess.run(
            ["python3", DEPLOY_CHECK_SCRIPT], 
            cwd=APP_DIR, 
            capture_output=True, 
            text=True
        )
        assert check_proc.returncode == 0, f"deploy_check.py failed with return code {check_proc.returncode}. Stderr: {check_proc.stderr}"

        # Verify diagnostic.json
        assert os.path.exists(DIAGNOSTIC_JSON), f"{DIAGNOSTIC_JSON} was not created by deploy_check.py."
        with open(DIAGNOSTIC_JSON, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"{DIAGNOSTIC_JSON} does not contain valid JSON.")

        assert data.get("check1") == 200, f"Expected 'check1' to be 200, got {data.get('check1')}."
        assert data.get("check2") == 200, f"Expected 'check2' to be 200, got {data.get('check2')}."

        # Verify restarts.log
        assert os.path.exists(RESTARTS_LOG), f"{RESTARTS_LOG} was not created by the supervisor script."
        with open(RESTARTS_LOG, 'r') as f:
            lines = f.read().strip().split('\n')

        assert len(lines) >= 1 and lines[0] != '', f"{RESTARTS_LOG} is empty, expected at least one restart timestamp."
        for line in lines:
            if line.strip():
                assert re.match(r'^[0-9]{10,}$', line.strip()), f"Invalid UNIX timestamp found in restarts.log: '{line}'"

    finally:
        # Cleanup processes
        subprocess.run(["pkill", "-f", "supervisor.sh"], capture_output=True)
        subprocess.run(["pkill", "-f", "server.py"], capture_output=True)
        try:
            supervisor_proc.kill()
            supervisor_proc.wait(timeout=1)
        except Exception:
            pass