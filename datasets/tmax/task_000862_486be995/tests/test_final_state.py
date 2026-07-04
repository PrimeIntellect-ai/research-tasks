# test_final_state.py
import os
import random
import subprocess
import tempfile
import csv

def generate_graph(num_nodes, num_edges):
    nodes = []
    types = ['User', 'Product', 'Category']
    for i in range(1, num_nodes + 1):
        nodes.append({
            'node_id': i,
            'node_type': random.choice(types),
            'weight': round(random.uniform(0.0, 100.0), 2)
        })

    edges = []
    rel_types = ['BUYS', 'BELONGS_TO', 'VIEWS']
    for _ in range(num_edges):
        source = random.randint(1, num_nodes)
        target = random.randint(1, num_nodes)
        edges.append({
            'source_id': source,
            'target_id': target,
            'relationship_type': random.choice(rel_types)
        })

    return nodes, edges

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_engine"
    agent_path = "/home/user/query_engine"

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle not executable"

    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}. Did you compile it?"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable."

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        nodes_file = os.path.join(tmpdir, "nodes.csv")
        edges_file = os.path.join(tmpdir, "edges.csv")

        for i in range(100):
            num_nodes = random.randint(50, 500)
            num_edges = random.randint(100, 2000)

            nodes, edges = generate_graph(num_nodes, num_edges)

            with open(nodes_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['node_id', 'node_type', 'weight'])
                writer.writeheader()
                writer.writerows(nodes)

            with open(edges_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['source_id', 'target_id', 'relationship_type'])
                writer.writeheader()
                writer.writerows(edges)

            offset = random.randint(0, 50)
            limit = random.randint(5, 100)

            cmd_oracle = [oracle_path, edges_file, nodes_file, str(offset), str(limit)]
            cmd_agent = [agent_path, edges_file, nodes_file, str(offset), str(limit)]

            res_oracle = subprocess.run(cmd_oracle, capture_output=True, text=True)
            res_agent = subprocess.run(cmd_agent, capture_output=True, text=True)

            assert res_oracle.returncode == 0, f"Oracle failed on iteration {i} with error:\n{res_oracle.stderr}"
            assert res_agent.returncode == 0, f"Agent program failed on iteration {i} with error:\n{res_agent.stderr}"

            if res_oracle.stdout != res_agent.stdout:
                msg = f"Mismatch on iteration {i}.\n"
                msg += f"Command: {' '.join(cmd_agent)}\n"
                msg += f"Oracle output:\n{res_oracle.stdout}\n"
                msg += f"Agent output:\n{res_agent.stdout}\n"
                assert False, msg