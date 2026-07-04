# test_final_state.py

import os
import subprocess
import random
import string
import tempfile
import shutil
import pytest

AGENT_SCRIPT = "/home/user/pack_ccf.py"
ORACLE_BINARY = "/app/legacy_cfg_manager"

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + "_", k=length))

def generate_random_file_content(size):
    if random.choice([True, False]):
        # ASCII
        return ''.join(random.choices(string.printable, k=size)).encode('utf-8')
    else:
        # Binary
        return os.urandom(size)

def create_random_directory_tree(base_dir):
    num_files = random.randint(1, 15)
    for _ in range(num_files):
        depth = random.randint(0, 4)
        current_dir = base_dir
        for _ in range(depth):
            dir_name = generate_random_string(random.randint(3, 12))
            current_dir = os.path.join(current_dir, dir_name)
            os.makedirs(current_dir, exist_ok=True)

        file_name = generate_random_string(random.randint(3, 12))
        file_path = os.path.join(current_dir, file_name)

        file_size = random.randint(0, 100 * 1024)
        content = generate_random_file_content(file_size)

        with open(file_path, 'wb') as f:
            f.write(content)

@pytest.fixture(scope="module")
def fuzz_env():
    random.seed(42)
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.path.exists(ORACLE_BINARY), f"Oracle binary missing at {ORACLE_BINARY}"
    return True

@pytest.mark.parametrize("iteration", range(50))
def test_fuzz_equivalence(fuzz_env, iteration):
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = os.path.join(temp_dir, "input")
        os.makedirs(input_dir)
        create_random_directory_tree(input_dir)

        oracle_output = os.path.join(temp_dir, "oracle.ccf")
        agent_output = os.path.join(temp_dir, "agent.ccf")

        # Run oracle
        oracle_cmd = [ORACLE_BINARY, "pack", input_dir, oracle_output]
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True)
        assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr.decode(errors='replace')}"
        assert os.path.exists(oracle_output), "Oracle did not produce output file"

        # Run agent
        agent_cmd = ["python3", AGENT_SCRIPT, input_dir, agent_output]
        agent_proc = subprocess.run(agent_cmd, capture_output=True)
        assert agent_proc.returncode == 0, f"Agent failed: {agent_proc.stderr.decode(errors='replace')}"
        assert os.path.exists(agent_output), "Agent did not produce output file"

        # Compare
        with open(oracle_output, "rb") as f:
            oracle_data = f.read()

        with open(agent_output, "rb") as f:
            agent_data = f.read()

        assert oracle_data == agent_data, f"Mismatch on iteration {iteration}. Output differs from oracle."