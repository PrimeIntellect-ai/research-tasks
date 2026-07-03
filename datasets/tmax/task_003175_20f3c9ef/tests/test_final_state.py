# test_final_state.py
import os
import re
import json
import time
import random
import subprocess
import pytest

def test_setup_env_script():
    script_path = "/home/user/setup_env.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_passwd_group_mock():
    passwd_path = "/home/user/passwd_mock"
    group_path = "/home/user/group_mock"

    assert os.path.isfile(passwd_path), f"{passwd_path} does not exist"
    assert os.path.isfile(group_path), f"{group_path} does not exist"

    with open(passwd_path, "r") as f:
        passwd_content = f.read()
    assert "cap-worker" in passwd_content, "cap-worker not found in passwd_mock"

    with open(group_path, "r") as f:
        group_content = f.read()
    assert "cap-planners" in group_content, "cap-planners not found in group_mock"

def test_telemetry_dirs():
    data_dir = "/home/user/telemetry_data"
    link_path = "/home/user/telemetry_link"

    assert os.path.isdir(data_dir), f"{data_dir} does not exist or is not a directory"
    assert os.path.islink(link_path), f"{link_path} is not a symlink"
    assert os.readlink(link_path) == data_dir, f"{link_path} does not point to {data_dir}"

def test_mock_fstab():
    fstab_path = "/home/user/mock_fstab"
    assert os.path.isfile(fstab_path), f"{fstab_path} does not exist"

    with open(fstab_path, "r") as f:
        content = f.read()

    # Expecting: tmpfs /home/user/telemetry_data tmpfs size=100M,gid=<mock_gid> 0 0
    assert re.search(r"tmpfs\s+/home/user/telemetry_data\s+tmpfs\s+size=100M,gid=\d+\s+0\s+0", content), "mock_fstab does not contain the correctly formatted tmpfs entry"

def test_scraper_output():
    log_path = "/home/user/scraper_output.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Services might not be running properly."

    # Wait a bit to ensure data is appended if just started
    time.sleep(2)

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "scraper_output.log is empty"

    # Check the last few lines for valid JSON
    valid_json_found = False
    for line in lines[-5:]:
        try:
            data = json.loads(line.strip())
            if data.get("status") == "ok" and "latest_cpu" in data:
                valid_json_found = True
                break
        except json.JSONDecodeError:
            continue

    assert valid_json_found, "Could not find valid JSON with 'status': 'ok' and 'latest_cpu' in the recent scraper output"

def test_fuzz_equivalence():
    agent_script = "/home/user/forecast_calc.py"
    oracle_bin = "/app/oracle_forecaster"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist"
    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} does not exist"

    random.seed(42)
    for _ in range(1000):
        cpu = random.randint(0, 100)
        mem = random.randint(0, 9999)
        io = random.randint(0, 999)
        input_str = f"CPU:{cpu} MEM:{mem} IO:{io}"

        oracle_proc = subprocess.run([oracle_bin, input_str], capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on input '{input_str}'"
        oracle_out = oracle_proc.stdout.strip()

        agent_proc = subprocess.run(["python3", agent_script, input_str], capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent script failed on input '{input_str}'"
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, f"Mismatch on input '{input_str}': oracle='{oracle_out}', agent='{agent_out}'"