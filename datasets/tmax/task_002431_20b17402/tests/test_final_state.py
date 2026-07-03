# test_final_state.py

import os
import json
import socket
import subprocess
import random
import pytest

def test_infrastructure_scripts_and_config():
    start_script = "/home/user/start_infrastructure.sh"
    config_file = "/home/user/bridge_config.json"

    assert os.path.isfile(start_script), f"Missing startup script: {start_script}"
    assert os.access(start_script, os.X_OK), f"Startup script is not executable: {start_script}"

    assert os.path.isfile(config_file), f"Missing config file: {config_file}"
    with open(config_file, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("bridge_config.json is not valid JSON")

    assert config.get("sensor_port") == 9001, "sensor_port is not 9001"
    assert config.get("cache_port") == 6379, "cache_port is not 6379"
    assert config.get("c2_port") == 9002, "c2_port is not 9002"

def test_services_running():
    expected_ports = {
        "Redis": 6379,
        "Sensor": 9001,
        "C2 Server": 9002
    }

    for name, port in expected_ports.items():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', port))
            assert result == 0, f"{name} service is not listening on port {port}"

def test_git_bisection():
    bad_commit_file = "/home/user/bad_commit.txt"
    repo_dir = "/home/user/bot_repo"

    assert os.path.isfile(bad_commit_file), f"Missing bad commit file: {bad_commit_file}"
    with open(bad_commit_file, 'r') as f:
        student_commit = f.read().strip()

    assert len(student_commit) == 40, "Commit hash should be exactly 40 characters"

    # Dynamically find the bad commit by looking for the bug injection
    commits_output = subprocess.check_output(
        ["git", "log", "--reverse", "--format=%H"], 
        cwd=repo_dir
    ).decode().strip().split('\n')

    actual_bad_commit = None
    for commit in commits_output:
        # Check the diff of each commit to see if it introduces the random failure
        diff = subprocess.check_output(
            ["git", "show", commit], 
            cwd=repo_dir, 
            errors="ignore"
        )
        if "rand" in diff or "segfault" in diff.lower() or "abort" in diff or "crash" in diff.lower():
            actual_bad_commit = commit
            break

    # Fallback to the 14th commit if we couldn't identify it via diff
    if not actual_bad_commit and len(commits_output) >= 14:
        actual_bad_commit = commits_output[13]

    if actual_bad_commit:
        assert student_commit == actual_bad_commit, f"Incorrect bad commit identified. Expected {actual_bad_commit}, got {student_commit}"

def test_decoder_fuzz_equivalence():
    oracle_path = "/app/oracle_decoder"
    agent_path = "/home/user/decoder.bin"

    assert os.path.isfile(agent_path), f"Missing agent decoder: {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent decoder is not executable: {agent_path}"

    rng = random.Random(1337)

    # Run 50 iterations with varying lengths to ensure equivalence without timing out pytest
    for i in range(50):
        length = rng.randint(1, 100000) # Test up to ~100KB
        input_data = os.urandom(length)

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert oracle_proc.returncode == 0, "Oracle decoder failed"
        assert agent_proc.returncode == 0, "Agent decoder failed"

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(f"Mismatch detected on fuzz iteration {i} with input length {length} bytes.")