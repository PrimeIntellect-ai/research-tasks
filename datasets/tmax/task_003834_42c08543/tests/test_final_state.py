# test_final_state.py

import os
import random
import string
import subprocess
import pytest

AGENT_EXE = "/home/user/exposure_calculator"
ORACLE_EXE = "/opt/oracle/exposure_calculator_oracle"
MAKEFILE_PATH = "/app/libgraphcsv-1.2.0/Makefile"
FUZZ_RUNS = 100  # Reduced from 500 to ensure tests run within reasonable time limits

def test_executable_exists():
    assert os.path.isfile(AGENT_EXE), f"Agent executable not found at {AGENT_EXE}"
    assert os.access(AGENT_EXE, os.X_OK), f"Agent file at {AGENT_EXE} is not executable"

def test_makefile_fixed():
    assert os.path.isfile(MAKEFILE_PATH), f"Makefile not found at {MAKEFILE_PATH}"
    with open(MAKEFILE_PATH, "r") as f:
        content = f.read()
    assert "-DMAX_RECURSION_DEPTH=3" not in content, "The deliberate perturbation in the Makefile was not fixed."

def generate_random_node_id():
    prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
    suffix = ''.join(random.choices(string.digits, k=3))
    return f"{prefix}_{suffix}"

def generate_fuzz_graph(num_nodes):
    nodes = list({generate_random_node_id() for _ in range(num_nodes)})
    num_nodes = len(nodes)

    edges = []
    types = ["ACCOUNT", "COMPANY", "OTHER"]

    # Ensure some connectivity
    for i in range(1, num_nodes):
        src = random.choice(nodes[:i])
        tgt = nodes[i]
        tgt_type = random.choice(types)
        weight = random.randint(1, 1000)
        edges.append((src, tgt, tgt_type, weight))

    # Add extra edges to create paths and cycles
    for _ in range(num_nodes * 3):
        src = random.choice(nodes)
        tgt = random.choice(nodes)
        if src != tgt:
            tgt_type = random.choice(types)
            weight = random.randint(1, 1000)
            edges.append((src, tgt, tgt_type, weight))

    return nodes, edges

@pytest.mark.parametrize("run_idx", range(FUZZ_RUNS))
def test_fuzz_equivalence(run_idx, tmp_path):
    random.seed(42 + run_idx)

    num_nodes = random.randint(50, 500)
    nodes, edges = generate_fuzz_graph(num_nodes)

    csv_path = tmp_path / f"fuzz_graph_{run_idx}.csv"
    with open(csv_path, "w") as f:
        for src, tgt, tgt_type, weight in edges:
            f.write(f"{src},{tgt},{tgt_type},{weight}\n")

    start_node = random.choice(nodes)

    # Run Oracle
    oracle_cmd = [ORACLE_EXE, str(csv_path), start_node]
    try:
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, timeout=5)
        oracle_out = oracle_res.stdout.strip()
    except Exception as e:
        pytest.fail(f"Oracle failed to run: {e}")

    # Run Agent
    agent_cmd = [AGENT_EXE, str(csv_path), start_node]
    try:
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, timeout=5)
        agent_out = agent_res.stdout.strip()
    except subprocess.TimeoutExpired:
        pytest.fail(f"Agent executable timed out on fuzz input {run_idx}.")
    except Exception as e:
        pytest.fail(f"Agent executable failed to run: {e}")

    assert agent_res.returncode == 0, f"Agent executable returned non-zero exit code {agent_res.returncode}. Stderr: {agent_res.stderr}"

    assert agent_out == oracle_out, (
        f"Output mismatch on fuzz run {run_idx}.\n"
        f"Start Node: {start_node}\n"
        f"Graph Size: {len(nodes)} nodes, {len(edges)} edges\n"
        f"Oracle Output: '{oracle_out}'\n"
        f"Agent Output: '{agent_out}'"
    )