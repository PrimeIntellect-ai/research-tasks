# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import random
import string
import tempfile
import time
import pytest

def test_sim_daemon_compiled():
    assert os.path.isfile("/app/sim/sim_daemon"), "sim_daemon executable not found at /app/sim/sim_daemon"
    assert os.access("/app/sim/sim_daemon", os.X_OK), "/app/sim/sim_daemon is not executable"

def test_services_running_and_pipeline():
    url = "http://127.0.0.1:9000/decompose"
    data = b"size=100"
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to API gateway at {url} or received bad response: {e}. Are all services running on the correct ports?")

    # Wait briefly for the telemetry logger to process the trace
    time.sleep(1.5)
    trace_file = "/app/logger/output.trace"
    assert os.path.isfile(trace_file), f"Telemetry logger did not write to {trace_file}. Is the pipeline correctly configured?"
    with open(trace_file, "r") as f:
        content = f.read()
        assert len(content.strip()) > 0, f"Trace file {trace_file} is empty."

def generate_dag(num_nodes, num_edges):
    # Generate unique node names
    nodes = set()
    while len(nodes) < num_nodes:
        nodes.add("Node" + "".join(random.choices(string.ascii_letters + string.digits, k=4)))
    nodes = list(nodes)

    edges = set()
    attempts = 0
    # Ensure we only pick (u, v) where index(u) < index(v) to guarantee a DAG
    while len(edges) < num_edges and attempts < num_edges * 10:
        attempts += 1
        u_idx = random.randint(0, num_nodes - 2)
        v_idx = random.randint(u_idx + 1, num_nodes - 1)
        edges.add((nodes[u_idx], nodes[v_idx]))

    lines = []
    for u, v in edges:
        latency = random.randint(1, 1000)
        lines.append(f"{u} {v} {latency}")
    return "\n".join(lines) + "\n"

def test_trace_analyzer_fuzz():
    agent_script = "/home/user/trace_analyzer.sh"
    oracle_bin = "/app/oracle_analyzer"

    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable"
    assert os.path.isfile(oracle_bin), f"Oracle binary missing at {oracle_bin}"

    random.seed(42)

    for i in range(500):
        num_nodes = random.randint(10, 50)
        num_edges = random.randint(15, 100)
        trace_data = generate_dag(num_nodes, num_edges)

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write(trace_data)
            tmp_path = tmp.name

        try:
            agent_res = subprocess.run([agent_script, tmp_path], capture_output=True, text=True, timeout=5)
            oracle_res = subprocess.run([oracle_bin, tmp_path], capture_output=True, text=True, timeout=5)

            agent_out = agent_res.stdout.strip()
            oracle_out = oracle_res.stdout.strip()

            if agent_out != oracle_out:
                pytest.fail(
                    f"Output mismatch on random DAG input (iteration {i+1}).\n\n"
                    f"Input Trace:\n{trace_data}\n"
                    f"Expected (Oracle):\n{oracle_out}\n\n"
                    f"Got (Agent):\n{agent_out}\n\n"
                    f"Agent STDERR:\n{agent_res.stderr}"
                )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input:\n{trace_data}")
        finally:
            os.remove(tmp_path)