# test_final_state.py
import os
import random
import string
import subprocess
import time

def test_port_mapper_fuzz_equivalence():
    oracle_path = "/app/port_mapper_oracle"
    agent_path = "/home/user/port_mapper.sh"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent script missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent script {agent_path} is not executable"

    random.seed(42)
    charset = string.ascii_lowercase + string.digits

    for _ in range(100):
        length = random.randint(4, 12)
        username = "".join(random.choice(charset) for _ in range(length))

        oracle_proc = subprocess.run([oracle_path, username], capture_output=True, text=True)
        agent_proc = subprocess.run(["/bin/bash", agent_path, username], capture_output=True, text=True)

        assert oracle_proc.returncode == 0, "Oracle execution failed"
        assert agent_proc.returncode == 0, f"Agent script failed on input '{username}'"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, f"Mismatch on input '{username}'. Oracle: {oracle_out}, Agent: {agent_out}"

def test_supervise_script_exists():
    agent_path = "/home/user/supervise.sh"
    assert os.path.isfile(agent_path), f"Supervise script missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Supervise script {agent_path} is not executable"

def test_deploy_script_exists():
    agent_path = "/home/user/deploy.sh"
    assert os.path.isfile(agent_path), f"Deploy script missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Deploy script {agent_path} is not executable"

def test_deploy_script_execution():
    username = "testuser123"
    oracle_proc = subprocess.run(["/app/port_mapper_oracle", username], capture_output=True, text=True)
    port = oracle_proc.stdout.strip()

    log_file = "/home/user/deploy.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    proc = subprocess.Popen(["/bin/bash", "/home/user/deploy.sh", username])

    success = False
    expected_log = f"Deployment successful for user: {username} on port: {port}"

    for _ in range(20):
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                content = f.read()
                if expected_log in content:
                    success = True
                    break
        time.sleep(0.5)

    # Clean up background processes created by the test
    proc.terminate()
    subprocess.run(["pkill", "-f", f"http.server {port}"])
    subprocess.run(["pkill", "-f", "supervise.sh"])

    assert success, f"Expected log entry '{expected_log}' not found in {log_file} within 10 seconds."