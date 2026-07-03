# test_final_state.py

import os
import sys
import json
import random
import string
import subprocess
import time
import socket
import tempfile
import pytest

ORACLE_PATH = "/app/sec_linker_oracle"
CLI_PATH = "/home/user/resolve_cli.py"
API_PATH = "/home/user/linker_api.py"

def wait_for_port(port, host='127.0.0.1', timeout=10.0):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.2)
    return False

def generate_graph(num_nodes, make_cyclic):
    nodes = set()
    while len(nodes) < num_nodes:
        name = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 8)))
        nodes.add(name)
    nodes = list(nodes)

    graph = {node: [] for node in nodes}

    # Create edges for a DAG
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < 0.3:
                graph[nodes[i]].append(nodes[j])

    if make_cyclic and num_nodes >= 2:
        # Create a cycle
        cycle_len = random.randint(2, num_nodes)
        cycle_nodes = random.sample(nodes, cycle_len)
        for i in range(cycle_len):
            u = cycle_nodes[i]
            v = cycle_nodes[(i + 1) % cycle_len]
            if v not in graph[u]:
                graph[u].append(v)

    return {"libraries": graph}

@pytest.fixture(scope="module")
def api_server():
    assert os.path.exists(API_PATH), f"API server file {API_PATH} not found"
    assert os.path.exists(CLI_PATH), f"CLI client file {CLI_PATH} not found"

    # Start API server
    proc = subprocess.Popen([sys.executable, API_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for port 8000
    if not wait_for_port(8000):
        proc.terminate()
        pytest.fail("API server did not start and listen on port 8000 within timeout.")

    yield

    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()

def test_fuzz_equivalence(api_server):
    random.seed(42)

    for i in range(200):
        num_nodes = random.randint(3, 50)
        make_cyclic = random.random() < 0.2
        graph_data = generate_graph(num_nodes, make_cyclic)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(graph_data, f)
            temp_path = f.name

        try:
            # Run oracle
            oracle_proc = subprocess.run([ORACLE_PATH, temp_path], capture_output=True, text=True)
            oracle_out = oracle_proc.stdout.strip()

            # Run agent
            agent_proc = subprocess.run([sys.executable, CLI_PATH, temp_path], capture_output=True, text=True)
            agent_out = agent_proc.stdout.strip()

            assert agent_out == oracle_out, (
                f"Mismatch on fuzz iteration {i+1}:\n"
                f"Input graph:\n{json.dumps(graph_data, indent=2)}\n\n"
                f"Oracle output:\n{oracle_out}\n\n"
                f"Agent output:\n{agent_out}\n"
                f"Agent stderr:\n{agent_proc.stderr}"
            )
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)