# test_final_state.py

import os
import subprocess
import random
import string
import tempfile
import pytest

def generate_random_dag(num_nodes):
    lines = []

    # Add random comments and blank lines
    for _ in range(random.randint(0, 5)):
        lines.append(f"# {random_string(10)}")
    for _ in range(random.randint(0, 5)):
        lines.append("")

    nodes = [f"V{i}" for i in range(num_nodes)]
    weights = {node: random.randint(1, 1000) for node in nodes}

    for node in nodes:
        lines.append(f"N {node} {weights[node]}")

    # Generate edges such that it forms a DAG (only edges from lower index to higher index)
    num_edges = random.randint(0, num_nodes * 2)
    for _ in range(num_edges):
        if num_nodes < 2:
            break
        src_idx = random.randint(0, num_nodes - 2)
        dst_idx = random.randint(src_idx + 1, num_nodes - 1)
        lines.append(f"E {nodes[src_idx]} {nodes[dst_idx]}")

    # Shuffle lines slightly, but nodes must be defined? The problem doesn't specify if nodes must be defined before edges.
    # We will just shuffle all lines. Wait, if we shuffle, it might be harder. Let's just shuffle.
    random.shuffle(lines)

    return "\n".join(lines) + "\n"

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def run_cmd(cmd, input_file):
    try:
        result = subprocess.run(
            cmd + [input_file],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return None, "Timeout", -1

def test_fuzz_equivalence():
    oracle_cmd = ["/app/graph_oracle"]
    agent_cmd = ["python3", "/home/user/cli.py"]

    assert os.path.exists("/home/user/cli.py"), "Agent CLI script missing."
    assert os.path.exists("/home/user/libgraph.so"), "Agent shared library missing."

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(200):
            num_nodes = random.randint(10, 1000)
            dag_str = generate_random_dag(num_nodes)

            input_file = os.path.join(tmpdir, f"graph_{i}.txt")
            with open(input_file, "w") as f:
                f.write(dag_str)

            oracle_out, oracle_err, oracle_rc = run_cmd(oracle_cmd, input_file)
            agent_out, agent_err, agent_rc = run_cmd(agent_cmd, input_file)

            assert oracle_rc == 0, f"Oracle failed on input {i}: {oracle_err}"
            assert agent_rc == 0, f"Agent failed on input {i}: {agent_err}\nInput:\n{dag_str}"

            assert oracle_out == agent_out, (
                f"Mismatch on iteration {i} (nodes: {num_nodes})\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output:  {agent_out}\n"
                f"Input graph:\n{dag_str}"
            )