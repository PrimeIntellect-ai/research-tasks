# test_final_state.py
import os
import subprocess
import random
import pytest

AGENT_BIN = "/home/user/engine/bin"
ORACLE_BIN = "/app/calc_engine"
FUZZ_N = 500

def generate_random_dag(seed):
    random.seed(seed)
    V = random.randint(10, 100)
    max_edges = V * (V - 1) // 4
    min_edges = V - 1
    if min_edges > max_edges:
        max_edges = min_edges
    E = random.randint(min_edges, max_edges)

    nodes = []
    for i in range(V):
        op_prob = random.random()
        if op_prob < 0.3:
            op = "INPUT"
            val = random.uniform(-50.0, 50.0)
            nodes.append(f"{i} {op} {val:.4f}")
        elif op_prob < 0.6:
            nodes.append(f"{i} ADD")
        elif op_prob < 0.8:
            nodes.append(f"{i} MUL")
        else:
            nodes.append(f"{i} MAX")

    edges = set()
    # To ensure no cycles, edges only go from smaller id to larger id
    while len(edges) < E:
        from_id = random.randint(0, V - 2)
        to_id = random.randint(from_id + 1, V - 1)
        edges.add((from_id, to_id))

    input_lines = [f"{V} {len(edges)}"]
    input_lines.extend(nodes)
    for from_id, to_id in edges:
        input_lines.append(f"{from_id} {to_id}")

    return "\n".join(input_lines) + "\n"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_BIN), f"Agent binary not found at {AGENT_BIN}"
    assert os.path.isfile(AGENT_BIN), f"Path {AGENT_BIN} is not a file"
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary at {AGENT_BIN} is not executable"

def test_oracle_exists():
    assert os.path.exists(ORACLE_BIN), f"Oracle binary not found at {ORACLE_BIN}"
    assert os.access(ORACLE_BIN, os.X_OK), f"Oracle binary at {ORACLE_BIN} is not executable"

@pytest.mark.parametrize("seed", range(FUZZ_N))
def test_fuzz_equivalence(seed):
    if not os.path.exists(AGENT_BIN):
        pytest.fail(f"Agent binary {AGENT_BIN} is missing.")

    dag_input = generate_random_dag(seed)

    oracle_proc = subprocess.run(
        [ORACLE_BIN],
        input=dag_input,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed on seed {seed}"

    agent_proc = subprocess.run(
        [AGENT_BIN],
        input=dag_input,
        text=True,
        capture_output=True
    )

    assert agent_proc.returncode == 0, f"Agent binary failed on seed {seed}. Stderr: {agent_proc.stderr}"

    oracle_out = oracle_proc.stdout.strip()
    agent_out = agent_proc.stdout.strip()

    if oracle_out != agent_out:
        pytest.fail(
            f"Mismatch on seed {seed}.\n"
            f"Input:\n{dag_input}\n"
            f"Expected (Oracle):\n{oracle_out}\n"
            f"Got (Agent):\n{agent_out}"
        )