# test_final_state.py

import os
import subprocess
import json
import random
import string
import tempfile
import pytest

ORACLE_BIN = "/home/user/bin/manifest_checker_ref"
AGENT_BIN = "/home/user/workspace/manifest_checker"
CRON_SCRIPT = "/home/user/cron/backup_job.sh"

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + "{}\":, \n\t", k=length))

def generate_valid_json():
    return json.dumps({
        "kind": random.choice(["Deployment", "Service", "Pod"]),
        "metadata": {
            "userGroup": random.choice(["admin", "dev", "test"]),
            "quotaLimit": random.randint(1, 1000)
        },
        "spec": {
            "replicas": random.randint(1, 10),
            "containers": [
                {
                    "name": generate_random_string(5),
                    "image": generate_random_string(10)
                }
            ]
        }
    })

def generate_invalid_json():
    # Randomly corrupt a valid JSON or just return random string
    if random.random() < 0.5:
        s = generate_valid_json()
        idx = random.randint(0, len(s)-1)
        return s[:idx] + s[idx+1:]
    else:
        return generate_random_string(random.randint(50, 4000))

def test_agent_binary_exists():
    assert os.path.isfile(AGENT_BIN), f"Agent binary not found at {AGENT_BIN}"
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary at {AGENT_BIN} is not executable"

def test_fuzz_equivalence():
    random.seed(42)
    N = 1000

    for i in range(N):
        if random.random() < 0.5:
            content = generate_valid_json()
        else:
            content = generate_invalid_json()

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as infile:
            infile.write(content)
            in_path = infile.name

        oracle_out_path = in_path + ".oracle.out"
        agent_out_path = in_path + ".agent.out"

        try:
            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_BIN, in_path, oracle_out_path],
                capture_output=True,
                text=True
            )

            # Run agent
            agent_proc = subprocess.run(
                [AGENT_BIN, in_path, agent_out_path],
                capture_output=True,
                text=True
            )

            # Read outputs if they exist
            oracle_out = ""
            if os.path.exists(oracle_out_path):
                with open(oracle_out_path, 'r') as f:
                    oracle_out = f.read()

            agent_out = ""
            if os.path.exists(agent_out_path):
                with open(agent_out_path, 'r') as f:
                    agent_out = f.read()

            assert oracle_proc.returncode == agent_proc.returncode, \
                f"Return code mismatch on input {content[:100]}...\nOracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

            assert oracle_out == agent_out, \
                f"Output file content mismatch on input {content[:100]}...\nOracle:\n{oracle_out}\nAgent:\n{agent_out}"

            assert oracle_proc.stdout == agent_proc.stdout, \
                f"STDOUT mismatch on input {content[:100]}...\nOracle:\n{oracle_proc.stdout}\nAgent:\n{agent_proc.stdout}"

        finally:
            if os.path.exists(in_path): os.remove(in_path)
            if os.path.exists(oracle_out_path): os.remove(oracle_out_path)
            if os.path.exists(agent_out_path): os.remove(agent_out_path)

def test_cron_script_fixes():
    assert os.path.isfile(CRON_SCRIPT), f"Cron script not found at {CRON_SCRIPT}"
    with open(CRON_SCRIPT, 'r') as f:
        content = f.read()

    assert "export PATH=/home/user/workspace:$PATH" in content or "PATH=/home/user/workspace" in content, \
        "Cron script does not correctly export PATH to include /home/user/workspace"

    assert "/home/user/backups/manifest.log" in content, \
        "Cron script does not redirect output to /home/user/backups/manifest.log"

    assert "QUOTA_API_URL=http://localhost:8081" in content, \
        "Cron script does not set QUOTA_API_URL=http://localhost:8081"

def test_end_to_end_flow():
    log_file = "/home/user/backups/manifest.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    result = subprocess.run(["bash", CRON_SCRIPT], capture_output=True, text=True)

    assert os.path.exists(log_file), f"Log file {log_file} was not created by the cron script."