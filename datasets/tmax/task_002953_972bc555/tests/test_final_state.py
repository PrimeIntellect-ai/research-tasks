# test_final_state.py

import os
import time
import subprocess
import random
import pytest

def test_diagnostic_seed_extracted():
    seed_file = "/home/user/diagnostic_seed.txt"
    assert os.path.isfile(seed_file), f"Seed file {seed_file} does not exist."
    with open(seed_file, "r") as f:
        content = f.read().strip()
    assert content == "A7F9B2C4", f"Expected seed 'A7F9B2C4', but got '{content}'."

def test_monitor_storage_script_exists_and_executable():
    script_path = "/home/user/monitor_storage.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_monitor_storage_logic():
    script_path = "/home/user/monitor_storage.sh"
    telemetry_dir = "/home/user/telemetry_data"
    mbox_path = "/home/user/admin_alerts.mbox"

    # Ensure telemetry dir exists
    os.makedirs(telemetry_dir, exist_ok=True)

    # Clear telemetry dir for test
    for f in os.listdir(telemetry_dir):
        os.remove(os.path.join(telemetry_dir, f))

    # Create files to exceed 50MB (6 files of 10MB)
    for i in range(6):
        with open(os.path.join(telemetry_dir, f"test_file_{i}.dat"), "wb") as f:
            f.write(os.urandom(10 * 1024 * 1024))
        # Sleep briefly to ensure distinct modification times
        time.sleep(0.05)

    # Get size before
    size_before = sum(os.path.getsize(os.path.join(telemetry_dir, f)) for f in os.listdir(telemetry_dir))
    assert size_before >= 50 * 1024 * 1024, "Failed to setup test files for storage monitor."

    # Run the script
    proc = subprocess.run([script_path], capture_output=True, text=True)
    assert proc.returncode == 0, f"Storage monitor script failed with error: {proc.stderr}"

    # Check size after
    size_after = sum(os.path.getsize(os.path.join(telemetry_dir, f)) for f in os.listdir(telemetry_dir))
    assert size_after < 40 * 1024 * 1024, f"Directory size {size_after} is not under 40MB after cleanup."

    # Check mbox alert
    assert os.path.isfile(mbox_path), f"Alert mbox {mbox_path} was not created."
    with open(mbox_path, "r") as f:
        content = f.read()
    assert "ALERT: Storage cleanup executed at" in content, "Alert message missing or incorrectly formatted in mbox."

def test_crontab_configured():
    proc = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert proc.returncode == 0, "Failed to read crontab. Has it been configured?"

    found = False
    for line in proc.stdout.strip().split('\n'):
        line = line.strip()
        if line.startswith('#'):
            continue
        if "/home/user/monitor_storage.sh" in line and ("*/5" in line or "0,5,10,15,20,25,30,35,40,45,50,55" in line):
            found = True
            break

    assert found, "Crontab does not contain the correct 5-minute schedule for monitor_storage.sh."

def test_acl_compiler_fuzz_equivalence():
    oracle_path = "/app/bin/legacy_acl_compiler"
    agent_path = "/home/user/acl_compiler"

    assert os.path.isfile(agent_path), f"Compiled agent binary {agent_path} not found."
    assert os.access(agent_path, os.X_OK), f"Agent binary {agent_path} is not executable."

    random.seed(1337)
    # Using N=1000 to prevent test timeout while still providing robust fuzzing
    N = 1000

    for i in range(N):
        length = random.randint(10, 500)
        test_input = bytes(random.getrandbits(8) for _ in range(length))

        oracle_proc = subprocess.run([oracle_path], input=test_input, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=test_input, capture_output=True)

        assert oracle_proc.returncode == agent_proc.returncode, f"Return code mismatch on input {test_input.hex()[:32]}..."
        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Output mismatch on input {test_input.hex()[:32]}...\n"
            f"Oracle output: {oracle_proc.stdout}\n"
            f"Agent output: {agent_proc.stdout}"
        )