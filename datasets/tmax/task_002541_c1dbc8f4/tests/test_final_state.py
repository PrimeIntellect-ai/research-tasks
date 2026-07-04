# test_final_state.py

import os
import csv
import random
import string
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/test/oracle.py"
AGENT_PATH = "/home/user/detect.py"
NUM_TESTS = 500

def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_csv(filepath):
    num_nodes = random.randint(10, 100)
    num_edges = random.randint(15, 300)

    nodes = [generate_random_string() for _ in range(num_nodes)]
    edges = set()

    for _ in range(num_edges):
        u = random.choice(nodes)
        v = random.choice(nodes)
        if u != v:
            edges.add((u, v))

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['tx', 'waiting_for'])
        for u, v in edges:
            writer.writerow([u, v])

    return nodes

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle program missing at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent script missing at {AGENT_PATH}"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, "graph.csv")

        for i in range(NUM_TESTS):
            nodes = generate_random_csv(csv_path)

            # Pick a random target node, sometimes one that might not be in the graph
            target_tx_id = random.choice(nodes) if random.random() < 0.9 else generate_random_string()

            oracle_cmd = ["python3", ORACLE_PATH, csv_path, target_tx_id]
            agent_cmd = ["python3", AGENT_PATH, csv_path, target_tx_id]

            oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
            agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)

            assert oracle_proc.returncode == 0, f"Oracle failed on test {i} with error:\n{oracle_proc.stderr}"

            oracle_out = oracle_proc.stdout.strip()
            agent_out = agent_proc.stdout.strip()

            if oracle_out != agent_out:
                with open(csv_path, 'r') as f:
                    csv_content = f.read()
                pytest.fail(
                    f"Mismatch on test {i}!\n"
                    f"Target TX ID: {target_tx_id}\n"
                    f"CSV Content:\n{csv_content}\n"
                    f"Oracle output: {oracle_out}\n"
                    f"Agent output: {agent_out}\n"
                    f"Agent stderr: {agent_proc.stderr}"
                )