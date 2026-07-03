# test_final_state.py

import os
import subprocess
import random
import string
import re
import pytest

def test_link_drops_count():
    path = "/home/user/link_drops.txt"
    assert os.path.exists(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "7", f"Expected '7' in {path}, but found '{content}'"

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_analyzer_oracle"
    agent_path = "/home/user/net_analyzer"

    assert os.path.exists(agent_path), f"Agent program missing: {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program is not executable: {agent_path}"

    random.seed(42)

    def generate_input():
        parts = []
        if random.random() < 0.5:
            parts.append(f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}")
        if random.random() < 0.5:
            parts.append(f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}")

        for _ in range(random.randint(1, 5)):
            parts.append(''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(2, 10))))

        random.shuffle(parts)
        res = " ".join(parts)
        if len(res) < 10:
            res += " " + ''.join(random.choices(string.ascii_letters, k=10))
        return res[:100]

    for i in range(1000):
        test_input = generate_input()

        oracle_proc = subprocess.run(
            [oracle_path], input=test_input, text=True, capture_output=True
        )
        agent_proc = subprocess.run(
            [agent_path], input=test_input, text=True, capture_output=True
        )

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {test_input}"
        assert agent_proc.returncode == 0, f"Agent failed on input: {test_input}"

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Mismatch on input: '{test_input}'\n"
            f"Oracle output: '{oracle_proc.stdout}'\n"
            f"Agent output: '{agent_proc.stdout}'"
        )

def test_expect_script_interaction():
    script_path = "/home/user/test_router.exp"
    assert os.path.exists(script_path), f"Expect script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Expect script is not executable: {script_path}"

    try:
        proc = subprocess.run(
            [script_path], capture_output=True, text=True, timeout=5
        )
        assert proc.returncode == 0, f"Expect script failed with return code {proc.returncode}\nStdout: {proc.stdout}\nStderr: {proc.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("Expect script timed out, likely hanging on a prompt.")

def test_monitoring_cron():
    cron_path = "/home/user/monitoring_cron"
    assert os.path.exists(cron_path), f"Cron file missing: {cron_path}"

    with open(cron_path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
    assert len(lines) > 0, "Cron file is empty or only contains comments"

    found_valid_cron = False
    for line in lines:
        parts = line.split()
        if len(parts) >= 6:
            minute, hour, dom, month, dow = parts[:5]
            cmd = " ".join(parts[5:])
            if "/home/user/test_router.exp" in cmd:
                if minute == "*/5" or minute == "0,5,10,15,20,25,30,35,40,45,50,55":
                    found_valid_cron = True
                    break

    assert found_valid_cron, f"Did not find a valid cron entry for every 5 minutes running /home/user/test_router.exp in {cron_path}"