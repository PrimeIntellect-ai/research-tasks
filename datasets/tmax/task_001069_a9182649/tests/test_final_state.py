# test_final_state.py

import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/graph_oracle"
AGENT_PATH = "/home/user/graph_eval.py"
N_FUZZ = 1000

def random_string(min_len=1, max_len=10):
    length = random.randint(min_len, max_len)
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_valid_dag(num_nodes, num_edges):
    nodes = [random_string() for _ in range(num_nodes)]
    # ensure unique nodes
    nodes = list(set(nodes))
    num_nodes = len(nodes)

    lines = []
    for node in nodes:
        latency = random.randint(1, 10000)
        lines.append(f"V {node} {latency}")

    edges = set()
    if num_nodes > 1:
        for _ in range(num_edges):
            u_idx = random.randint(0, num_nodes - 2)
            v_idx = random.randint(u_idx + 1, num_nodes - 1)
            edges.add((nodes[u_idx], nodes[v_idx]))

    for u, v in edges:
        lines.append(f"E {u} {v}")

    random.shuffle(lines)
    return "\n".join(lines) + "\n"

def generate_cyclic_graph(num_nodes, num_edges):
    if num_nodes < 2:
        num_nodes = 2
    nodes = [random_string() for _ in range(num_nodes)]
    nodes = list(set(nodes))
    num_nodes = len(nodes)

    lines = []
    for node in nodes:
        latency = random.randint(1, 10000)
        lines.append(f"V {node} {latency}")

    # Create a guaranteed cycle
    cycle_len = random.randint(2, num_nodes)
    cycle_nodes = random.sample(nodes, cycle_len)
    for i in range(cycle_len):
        u = cycle_nodes[i]
        v = cycle_nodes[(i + 1) % cycle_len]
        lines.append(f"E {u} {v}")

    random.shuffle(lines)
    return "\n".join(lines) + "\n"

def generate_undeclared_nodes(num_nodes, num_edges):
    nodes = [random_string() for _ in range(num_nodes)]
    nodes = list(set(nodes))
    num_nodes = len(nodes)

    lines = []
    for node in nodes:
        latency = random.randint(1, 10000)
        lines.append(f"V {node} {latency}")

    undeclared = random_string(11, 15) # Guaranteed not in nodes if max_len=10
    if nodes:
        lines.append(f"E {nodes[0]} {undeclared}")
    else:
        lines.append(f"E {undeclared} {random_string(11, 15)}")

    random.shuffle(lines)
    return "\n".join(lines) + "\n"

def generate_malformed():
    choices = [
        "V missing_latency",
        "V NODE -5",
        "V NODE 0",
        "E NODE",
        "RANDOM GARBAGE",
        "V NODE 10\nE NODE",
    ]
    return random.choice(choices) + "\n"

def generate_input():
    r = random.random()
    num_nodes = random.randint(1, 50)
    num_edges = random.randint(0, 100)

    if r < 0.70:
        return generate_valid_dag(num_nodes, num_edges)
    elif r < 0.80:
        return generate_cyclic_graph(num_nodes, num_edges)
    elif r < 0.90:
        return generate_undeclared_nodes(num_nodes, num_edges)
    else:
        return generate_malformed()

def run_cmd(cmd, input_data):
    proc = subprocess.run(
        cmd,
        input=input_data.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return proc.stdout.decode('utf-8')

def test_graph_eval_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent script missing at {AGENT_PATH}"

    random.seed(42)

    for i in range(N_FUZZ):
        input_data = generate_input()

        oracle_out = run_cmd([ORACLE_PATH], input_data)
        agent_out = run_cmd(["python3", AGENT_PATH], input_data)

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input:\n{input_data}\n"
                f"Oracle Output:\n{oracle_out}\n"
                f"Agent Output:\n{agent_out}\n"
            )