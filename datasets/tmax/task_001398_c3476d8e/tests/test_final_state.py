# test_final_state.py
import os
import random
import subprocess
import tempfile
import pytest
from datetime import datetime, timedelta

def test_health_log_up():
    log_file = "/home/user/logs/health.log"
    assert os.path.exists(log_file), f"Log file {log_file} does not exist."
    with open(log_file, "r") as f:
        lines = f.readlines()

    # The health checker runs every second. Check the last 15 lines for at least one 'UP' entry.
    recent_lines = lines[-15:]
    up_count = sum(1 for line in recent_lines if "| UP |" in line)
    assert up_count > 0, (
        "No recent 'UP' entries found in health.log. "
        "This indicates Nginx is not routing /ping to the backend correctly, "
        "or the git hook failed to reload Nginx."
    )

def test_git_hook():
    hook_path = "/home/user/nginx.git/hooks/post-receive"
    assert os.path.exists(hook_path), f"Git hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable."

def generate_log_file(path, num_lines):
    with open(path, 'w') as f:
        dt = datetime(2023, 10, 4, 12, 0, 0)
        for _ in range(num_lines):
            dt += timedelta(seconds=random.randint(1, 10))
            dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            if random.choice([True, False]):
                status = "UP"
                latency = random.randint(0, 5000)
            else:
                status = "DOWN"
                latency = -1
            f.write(f"{dt_str} | {status} | {latency}\n")

def test_parser_fuzz_equivalence():
    agent_parser = "/home/user/parser"
    oracle_parser = "/app/oracle_parser"

    assert os.path.exists(agent_parser), f"Parser executable missing at {agent_parser}"
    assert os.access(agent_parser, os.X_OK), f"Parser at {agent_parser} is not executable"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(100):
            num_lines = random.randint(10, 500)
            log_path = os.path.join(tmpdir, f"test_{i}.log")
            generate_log_file(log_path, num_lines)

            oracle_proc = subprocess.run([oracle_parser, log_path], capture_output=True)
            agent_proc = subprocess.run([agent_parser, log_path], capture_output=True)

            assert agent_proc.returncode == oracle_proc.returncode, (
                f"Return code mismatch on input {log_path}. "
                f"Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"
            )

            if agent_proc.stdout != oracle_proc.stdout:
                with open(log_path, 'r') as f:
                    sample_input = f.read()
                pytest.fail(
                    f"Output mismatch on input {log_path}.\n"
                    f"Input sample (first 100 chars): {sample_input[:100]}...\n"
                    f"Oracle output (hex): {oracle_proc.stdout.hex()}\n"
                    f"Agent output (hex): {agent_proc.stdout.hex()}"
                )