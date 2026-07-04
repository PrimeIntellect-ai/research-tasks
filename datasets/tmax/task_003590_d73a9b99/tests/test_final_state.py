# test_final_state.py

import os
import random
import subprocess
import json

def test_scene_changes_count():
    """Verify that the scene changes count is correct."""
    output_path = "/home/user/scene_changes.txt"
    assert os.path.isfile(output_path), f"File not found: {output_path}"

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "14", f"Expected scene change count to be 14, but got: {content}"

def test_graph_projector_fuzz_equivalence():
    """Fuzz test the Rust binary against the oracle."""
    agent_bin = "/home/user/graph_projector/target/release/graph_projector"
    oracle_bin = "/opt/oracle/graph_projector_bin"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    random.seed(42)

    for i in range(100):
        num_rows = random.randint(10, 1000)
        csv_lines = []
        for _ in range(num_rows):
            c0 = random.randint(1, 100)
            c1 = random.randint(1, 100)
            c2 = random.uniform(0.0, 2.0)
            c3 = random.randint(1, 1000)
            csv_lines.append(f"{c0},{c1},{c2:.4f},{c3}")

        csv_data = "\n".join(csv_lines) + "\n"

        # Run agent
        agent_proc = subprocess.run(
            [agent_bin],
            input=csv_data,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent binary failed on iteration {i}:\n{agent_proc.stderr}"

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=csv_data,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle binary failed on iteration {i}:\n{oracle_proc.stderr}"

        # Parse JSON to avoid whitespace differences
        try:
            agent_json = json.loads(agent_proc.stdout.strip())
        except json.JSONDecodeError:
            assert False, f"Agent output is not valid JSON:\n{agent_proc.stdout}"

        try:
            oracle_json = json.loads(oracle_proc.stdout.strip())
        except json.JSONDecodeError:
            assert False, f"Oracle output is not valid JSON:\n{oracle_proc.stdout}"

        assert agent_json == oracle_json, (
            f"Mismatch on iteration {i}.\n"
            f"Input CSV:\n{csv_data}\n"
            f"Expected (Oracle):\n{oracle_json}\n"
            f"Got (Agent):\n{agent_json}"
        )