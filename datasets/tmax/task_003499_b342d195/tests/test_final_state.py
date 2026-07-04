# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_video_summary_output():
    summary_path = "/home/user/video_summary.json"
    assert os.path.exists(summary_path), f"Missing {summary_path}"

    with open(summary_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON.")

    expected = {"1709996400": 2, "1710003600": 2}
    assert data == expected, f"Expected {expected}, got {data}"

def test_cron_job_configured():
    try:
        # Check crontab for user 'user'
        result = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True)
        crontab_content = result.stdout
    except Exception as e:
        pytest.fail(f"Failed to read crontab for user: {e}")

    expected_cmd = "*/15 * * * * python3 /home/user/text_bucketer.py < /tmp/input.log > /tmp/output.json"

    # Check if the exact command is in the crontab
    found = any(expected_cmd in line for line in crontab_content.splitlines())
    assert found, f"Cron job not found or incorrect. Expected to find: {expected_cmd}"

def test_fuzz_equivalence():
    agent_script = "/home/user/text_bucketer.py"
    oracle_bin = "/app/oracle_bucketer"

    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"
    assert os.path.exists(oracle_bin), f"Oracle binary missing at {oracle_bin}"

    random.seed(42)

    for i in range(1000):
        if random.random() < 0.7:
            ts = str(random.randint(0, 2000000000)).encode('ascii')
            msg_len = random.randint(10, 480)
            msg = bytearray(random.getrandbits(8) for _ in range(msg_len))
            payload = ts + b"|" + msg + b"\n"
        else:
            length = random.randint(10, 500)
            payload = bytearray(random.getrandbits(8) for _ in range(length)) + b"\n"

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=payload,
            capture_output=True
        )

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=payload,
            capture_output=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on input {payload[:50]}..."

        # Compare stdout
        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on fuzz iteration {i}.\n"
            f"Input (hex): {payload.hex()[:100]}...\n"
            f"Oracle: {oracle_out}\n"
            f"Agent:  {agent_out}"
        )