# test_final_state.py
import os
import random
import subprocess
import pytest

def test_bash_profile():
    profile_path = "/home/user/.bash_profile"
    assert os.path.exists(profile_path), f"File {profile_path} is missing."
    with open(profile_path, "r") as f:
        content = f.read()
    assert "TZ=Pacific/Honolulu" in content, "TZ=Pacific/Honolulu not found in .bash_profile"
    assert "DEVICE_ID=CAM_EDGE_01" in content, "DEVICE_ID=CAM_EDGE_01 not found in .bash_profile"

def test_edge_conf():
    conf_path = "/home/user/edge.conf"
    assert os.path.exists(conf_path), f"File {conf_path} is missing."
    with open(conf_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    assert "THRESHOLD=80" in lines, "THRESHOLD=80 not found in edge.conf"
    assert "ADMIN_EMAIL=admin@iot.local" in lines, "ADMIN_EMAIL=admin@iot.local not found in edge.conf"

def test_glitch_frames():
    frames_path = "/home/user/glitch_frames.txt"
    assert os.path.exists(frames_path), f"File {frames_path} is missing."
    with open(frames_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    expected = ["23", "89", "142"]
    assert lines == expected, f"Expected glitch frames {expected}, but got {lines}"

def test_edge_cron():
    cron_path = "/home/user/edge_cron"
    assert os.path.exists(cron_path), f"File {cron_path} is missing."
    with open(cron_path, "r") as f:
        content = f.read()
    assert "*/15 * * * *" in content, "Cron schedule */15 * * * * not found in edge_cron"
    assert "/home/user/log_processor < /var/log/sensor.log >> /var/log/processed.log" in content, "Cron command not found in edge_cron"

def test_fuzz_equivalence():
    agent_bin = "/home/user/log_processor"
    oracle_bin = "/app/oracle_processor"

    assert os.path.exists(agent_bin), f"Agent binary {agent_bin} is missing."
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."
    assert os.path.exists(oracle_bin), f"Oracle binary {oracle_bin} is missing."

    random.seed(42)
    env = os.environ.copy()
    env["TZ"] = "Pacific/Honolulu"
    env["DEVICE_ID"] = "CAM_EDGE_01"

    for _ in range(50):
        num_lines = random.randint(1, 1000)
        input_lines = []
        for _ in range(num_lines):
            ts = random.randint(1600000000, 1750000000)
            val = random.randint(0, 100)
            input_lines.append(f"{ts} {val}")

        input_data = "\n".join(input_lines) + "\n"

        oracle_proc = subprocess.run(
            [oracle_bin], input=input_data, text=True, capture_output=True, env=env
        )
        agent_proc = subprocess.run(
            [agent_bin], input=input_data, text=True, capture_output=True, env=env
        )

        assert oracle_proc.returncode == agent_proc.returncode, "Return codes differ between oracle and agent"
        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Outputs differ!\n"
            f"Input (first 5 lines): {input_data.splitlines()[:5]}\n"
            f"Oracle Output (first 5 lines): {oracle_proc.stdout.splitlines()[:5]}\n"
            f"Agent Output (first 5 lines): {agent_proc.stdout.splitlines()[:5]}"
        )