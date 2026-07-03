# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/oracle/graph_analyzer.sh"
AGENT_PATH = "/home/user/graph_analyzer.sh"
NUM_TESTS = 100

def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_graph():
    num_nodes = random.randint(50, 500)
    nodes = [generate_random_string() for _ in range(num_nodes)]
    edges = []

    for node in nodes:
        num_out_edges = random.randint(2, 10)
        targets = random.choices(nodes, k=num_out_edges)
        for target in targets:
            edges.append(f"{node} {target}")

    return "\n".join(edges), random.choice(nodes)

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_PATH), f"Agent script {AGENT_PATH} does not exist."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script {AGENT_PATH} is not executable."

def test_makefile_fixed():
    # Check if make install works
    result = subprocess.run(["make", "install"], cwd="/app/sh-graph-tools", capture_output=True)
    assert result.returncode == 0, f"make install failed:\nSTDOUT:\n{result.stdout.decode()}\nSTDERR:\n{result.stderr.decode()}"
    assert os.path.isfile("/app/sh-graph-tools/bin/dfs.sh"), "/app/sh-graph-tools/bin/dfs.sh does not exist after make install."
    assert os.access("/app/sh-graph-tools/bin/dfs.sh", os.X_OK), "/app/sh-graph-tools/bin/dfs.sh is not executable."

def test_fuzz_equivalence():
    random.seed(42)

    for i in range(NUM_TESTS):
        graph_content, start_node = generate_random_graph()
        input_file = f"/tmp/fuzz_graph_{i}.txt"
        with open(input_file, "w") as f:
            f.write(graph_content)

        oracle_cmd = [ORACLE_PATH, input_file, start_node]
        agent_cmd = [AGENT_PATH, input_file, start_node]

        oracle_result = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_result = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_result.returncode == 0, f"Oracle failed on test {i} with error: {oracle_result.stderr}"

        if oracle_result.stdout != agent_result.stdout:
            error_msg = f"Output mismatch on test {i} (start node: {start_node}).\n"
            error_msg += f"Oracle output:\n{oracle_result.stdout}\n"
            error_msg += f"Agent output:\n{agent_result.stdout}\n"
            error_msg += f"Agent stderr:\n{agent_result.stderr}\n"
            pytest.fail(error_msg)

        os.remove(input_file)