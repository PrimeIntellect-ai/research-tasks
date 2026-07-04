# test_final_state.py

import os
import random
import string
import subprocess
import shutil
import pytest

ORACLE_PATH = "/app/doc_packager"
AGENT_SCRIPT = "/home/user/doc_packager_replica.py"
FUZZ_BASE = "/tmp/fuzz_dirs"
MNT_EXT = "/mnt/fuzz_ext"

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_random_structure(base_dir, num_nodes):
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(MNT_EXT, exist_ok=True)

    dirs = [base_dir]
    all_nodes = []

    for i in range(num_nodes):
        parent = random.choice(dirs)
        node_name = f"node_{i}_{generate_random_string(4)}"
        node_path = os.path.join(parent, node_name)

        node_type = random.choices(['file', 'dir', 'symlink'], weights=[50, 20, 30])[0]

        if node_type == 'dir':
            os.mkdir(node_path)
            dirs.append(node_path)
            all_nodes.append(node_path)
        elif node_type == 'file':
            size = random.randint(0, 1024)
            content = generate_random_string(size)
            with open(node_path, 'w') as f:
                f.write(content)
            all_nodes.append(node_path)
        elif node_type == 'symlink':
            link_type = random.choices(['valid', 'cycle', 'broken', 'ext'], weights=[50, 20, 10, 20])[0]
            if link_type == 'valid' and all_nodes:
                target = random.choice(all_nodes)
            elif link_type == 'cycle':
                target = parent # Creates a cycle
            elif link_type == 'broken':
                target = os.path.join(base_dir, "nonexistent_target")
            else: # ext
                target = os.path.join(MNT_EXT, f"ext_target_{i}")
                with open(target, 'w') as f:
                    f.write("ext")

            # Use relative or absolute? The prompt doesn't specify, let's use absolute for simplicity
            os.symlink(target, node_path)
            all_nodes.append(node_path)

@pytest.mark.parametrize("seed", range(20))
def test_fuzz_equivalence(seed):
    random.seed(seed)

    assert os.path.exists(ORACLE_PATH), "Oracle binary not found."
    assert os.path.exists(AGENT_SCRIPT), "Agent script not found."

    test_dir = os.path.join(FUZZ_BASE, f"test_{seed}")
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    num_nodes = random.randint(10, 50)
    create_random_structure(test_dir, num_nodes)

    oracle_out = os.path.join(FUZZ_BASE, f"oracle_{seed}.archive")
    agent_out = os.path.join(FUZZ_BASE, f"agent_{seed}.archive")

    # Run oracle
    oracle_proc = subprocess.run([ORACLE_PATH, test_dir, oracle_out], capture_output=True)
    assert oracle_proc.returncode == 0, f"Oracle failed on seed {seed}: {oracle_proc.stderr}"

    # Run agent
    agent_proc = subprocess.run(["python3", AGENT_SCRIPT, test_dir, agent_out], capture_output=True)
    assert agent_proc.returncode == 0, f"Agent script failed on seed {seed}: {agent_proc.stderr.decode('utf-8', errors='replace')}"

    assert os.path.exists(oracle_out), "Oracle did not produce an output file."
    assert os.path.exists(agent_out), "Agent did not produce an output file."

    with open(oracle_out, 'rb') as f1, open(agent_out, 'rb') as f2:
        oracle_data = f1.read()
        agent_data = f2.read()

    if oracle_data != agent_data:
        pytest.fail(f"Mismatch on seed {seed}.\nOracle output size: {len(oracle_data)}\nAgent output size: {len(agent_data)}")