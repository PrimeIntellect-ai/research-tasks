# test_final_state.py

import os
import subprocess
import random
import pytest
import urllib.request
import urllib.error

def test_dataset_downloaded():
    dataset_path = '/home/user/dataset.txt'
    assert os.path.isfile(dataset_path), f"Dataset file {dataset_path} is missing."

    with open(dataset_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 100, f"Expected 100 lines in {dataset_path}, found {len(lines)}."
    for line in lines:
        try:
            float(line)
        except ValueError:
            pytest.fail(f"Line '{line}' in {dataset_path} is not a valid float.")

def test_services_running_and_proxying():
    try:
        req = urllib.request.Request('http://localhost:8080/dataset')
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read().decode('utf-8').strip().split('\n')
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to fetch dataset from http://localhost:8080/dataset: {e}")

    assert len(data) == 100, f"Expected 100 lines from API, got {len(data)}."

    # Check if it matches the downloaded dataset
    dataset_path = '/home/user/dataset.txt'
    if os.path.isfile(dataset_path):
        with open(dataset_path, 'r') as f:
            local_data = f.read().strip().split('\n')
        assert data == local_data, "Data from API does not match /home/user/dataset.txt"

def test_bootstrapper_binary_exists():
    binary_path = '/home/user/bootstrapper'
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_fuzz_equivalence():
    agent_binary = '/home/user/bootstrapper'
    oracle_binary = '/app/oracle_bootstrapper'

    assert os.path.isfile(oracle_binary), f"Oracle binary {oracle_binary} is missing."
    assert os.access(oracle_binary, os.X_OK), f"Oracle binary {oracle_binary} is not executable."

    random.seed(42)
    num_tests = 20

    for _ in range(num_tests):
        seed = random.randint(1, 100000)
        B = random.randint(1000, 5000)

        agent_cmd = [agent_binary, str(seed), str(B)]
        oracle_cmd = [oracle_binary, str(seed), str(B)]

        try:
            agent_result = subprocess.run(agent_cmd, capture_output=True, text=True, timeout=5, check=True)
            agent_output = agent_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent binary failed on input {seed} {B}:\n{e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on input {seed} {B}")

        try:
            oracle_result = subprocess.run(oracle_cmd, capture_output=True, text=True, timeout=5, check=True)
            oracle_output = oracle_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle binary failed on input {seed} {B}:\n{e.stderr}")

        assert agent_output == oracle_output, (
            f"Mismatch on inputs seed={seed}, B={B}.\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )