# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    agent_script = "/home/user/project_graph.py"
    oracle_bin = "/app/graph_materializer_bin"

    assert os.path.exists(agent_script), f"Agent script {agent_script} not found."
    assert os.path.exists(oracle_bin), f"Oracle binary {oracle_bin} not found."

    random.seed(42)

    tables = ["Users", "Departments", "Roles", "Projects"]

    for _ in range(50):
        src = random.choice(tables)
        tgt = random.choice(tables)
        link = f"{src}_TO_{tgt}"

        # Provide both sets of keys mentioned in the prompt to ensure compatibility
        payload = {
            "source": src,
            "target": tgt,
            "link": link,
            "source_table": src,
            "target_table": tgt,
            "relation_type": link
        }

        input_json = json.dumps(payload).encode('utf-8')

        oracle_proc = subprocess.run([oracle_bin], input=input_json, capture_output=True)
        agent_proc = subprocess.run(["python3", agent_script], input=input_json, capture_output=True)

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Return code mismatch for input {payload}: "
            f"oracle={oracle_proc.returncode}, agent={agent_proc.returncode}.\n"
            f"Agent stderr: {agent_proc.stderr.decode('utf-8')}"
        )

        oracle_out = oracle_proc.stdout.decode('utf-8')
        agent_out = agent_proc.stdout.decode('utf-8')

        assert oracle_out == agent_out, (
            f"Output mismatch for input {payload}.\n"
            f"Oracle output (first 500 chars):\n{oracle_out[:500]}\n"
            f"Agent output (first 500 chars):\n{agent_out[:500]}"
        )