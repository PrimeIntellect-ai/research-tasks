# test_final_state.py
import os
import random
import string
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/graph_oracle"
AGENT_PATH = "/home/user/graph_tool/target/release/graph_tool"
NUM_ITERATIONS = 50
EDGE_TYPES = ["KNOWS", "LIKES", "FOLLOWS", "BLOCKS", "TRUSTS"]

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def run_program(executable, nodes_file, edges_file, stdin_data):
    try:
        result = subprocess.run(
            [executable, nodes_file, edges_file],
            input=stdin_data,
            text=True,
            capture_output=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"

@pytest.mark.parametrize("iteration", range(NUM_ITERATIONS))
def test_fuzz_equivalence(iteration):
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary is not executable: {AGENT_PATH}"

    # Use a fixed seed based on iteration for reproducibility
    random.seed(42 + iteration)

    num_nodes = random.randint(100, 1000)
    num_edges = random.randint(500, 5000)

    nodes = []
    for _ in range(num_nodes):
        node_id = generate_random_string(random.randint(4, 8))
        weight = random.randint(-100, 1000)
        nodes.append((node_id, weight))

    # Ensure unique node IDs
    node_dict = {n[0]: n[1] for n in nodes}
    node_ids = list(node_dict.keys())

    edges = []
    for _ in range(num_edges):
        src = random.choice(node_ids)
        dst = random.choice(node_ids)
        etype = random.choice(EDGE_TYPES)
        edges.append((src, dst, etype))

    queries = []
    for _ in range(100):
        # Occasionally use a non-existent ID
        if random.random() < 0.05:
            start_node = generate_random_string(10)
        else:
            start_node = random.choice(node_ids)

        num_steps = random.randint(0, 5)
        query_parts = [start_node] + [random.choice(EDGE_TYPES) for _ in range(num_steps)]
        queries.append(",".join(query_parts))

    stdin_data = "\n".join(queries) + "\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        nodes_file = os.path.join(tmpdir, "nodes.csv")
        edges_file = os.path.join(tmpdir, "edges.csv")

        with open(nodes_file, "w") as f:
            for node_id, weight in node_dict.items():
                f.write(f"{node_id},{weight}\n")

        with open(edges_file, "w") as f:
            for src, dst, etype in edges:
                f.write(f"{src},{dst},{etype}\n")

        oracle_code, oracle_out, oracle_err = run_program(ORACLE_PATH, nodes_file, edges_file, stdin_data)
        agent_code, agent_out, agent_err = run_program(AGENT_PATH, nodes_file, edges_file, stdin_data)

        assert agent_code == oracle_code, (
            f"Exit code mismatch on iteration {iteration}.\n"
            f"Oracle: {oracle_code}, Agent: {agent_code}\n"
            f"Agent stderr: {agent_err}"
        )

        if oracle_out != agent_out:
            # Truncate output for display if it's too long
            display_oracle = oracle_out[:1000] + ("..." if len(oracle_out) > 1000 else "")
            display_agent = agent_out[:1000] + ("..." if len(agent_out) > 1000 else "")
            pytest.fail(
                f"Stdout mismatch on iteration {iteration}.\n"
                f"--- Oracle Output ---\n{display_oracle}\n"
                f"--- Agent Output ---\n{display_agent}\n"
            )