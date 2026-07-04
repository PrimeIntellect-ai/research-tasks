# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_fuzz_input(num_lines):
    lines = []
    ts = 1700000000
    sensors = ["S1", "S2", "TEMP_A", "HUMID_B", "X9"]
    for _ in range(num_lines):
        ts += random.randint(1, 25)
        sensor = random.choice(sensors)
        val = random.randint(-100, 100)
        lines.append(f"{ts},{sensor},{val}")
    return "\n".join(lines) + "\n"

def test_fuzz_cleaner_equivalence():
    oracle_path = "/app/oracle/legacy_cleaner"
    agent_path = "/home/user/cleaner"

    assert os.path.exists(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary not executable at {agent_path}"

    random.seed(42)
    for i in range(500):
        num_lines = random.randint(10, 1000)
        input_data = generate_fuzz_input(num_lines)

        oracle_proc = subprocess.run([oracle_path], input=input_data, text=True, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, text=True, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on test case {i}"
        assert agent_proc.returncode == 0, f"Agent failed on test case {i}. Stderr: {agent_proc.stderr}"

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Output mismatch on test case {i}.\n"
                f"Input preview:\n{input_data[:200]}...\n\n"
                f"Oracle output preview:\n{oracle_proc.stdout[:200]}...\n\n"
                f"Agent output preview:\n{agent_proc.stdout[:200]}..."
            )

def test_pipeline_script():
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"{script_path} missing"
    assert os.access(script_path, os.X_OK), f"{script_path} not executable"

    # Clear redis list to ensure we are testing a fresh run
    subprocess.run(["redis-cli", "DEL", "sensor_data_cleaned"], check=True)

    # Run pipeline
    proc = subprocess.run([script_path], capture_output=True, text=True)
    assert proc.returncode == 0, f"pipeline.sh failed to execute. Stderr: {proc.stderr}"

    # Check redis
    res = subprocess.run(["redis-cli", "LLEN", "sensor_data_cleaned"], capture_output=True, text=True, check=True)
    llen = int(res.stdout.strip())
    assert llen > 0, "Redis list 'sensor_data_cleaned' is empty after running pipeline.sh. Ensure it pipes output to Redis."

def test_cron_job():
    cron_file = "/var/spool/cron/crontabs/user"
    content = ""
    if os.path.exists(cron_file):
        with open(cron_file, "r") as f:
            content = f.read()
    else:
        res = subprocess.run(["crontab", "-u", "user", "-l"], capture_output=True, text=True)
        content = res.stdout

    assert "/home/user/pipeline.sh" in content, "Cron job for /home/user/pipeline.sh not found for user 'user'"

    found_every_minute = False
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "/home/user/pipeline.sh" in line:
            parts = line.split()
            if parts[:5] == ["*", "*", "*", "*", "*"]:
                found_every_minute = True
                break

    assert found_every_minute, "Cron job is not scheduled to run every minute ('* * * * *')"