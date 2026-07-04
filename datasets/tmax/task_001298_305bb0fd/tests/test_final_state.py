# test_final_state.py
import os
import subprocess
import random
import pytest

def test_audit_query_exists():
    agent_script = "/home/user/audit_query.sh"
    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."

def test_fuzz_equivalence():
    agent_script = "/home/user/audit_query.sh"
    oracle_bin = "/app/access_oracle"
    graph_file = "/app/access_graph.tsv"

    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} is missing."
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable."
    assert os.path.isfile(graph_file), f"Graph file {graph_file} is missing."

    sources = set()
    targets = set()
    with open(graph_file, "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                sources.add(parts[0])
                targets.add(parts[1])

    assert sources, "No source nodes found in the graph."
    assert targets, "No target nodes found in the graph."

    sources = sorted(list(sources))
    targets = sorted(list(targets))

    random.seed(42)
    N = 100

    for _ in range(N):
        src = random.choice(sources)
        tgt = random.choice(targets)

        # Run Oracle
        oracle_cmd = [oracle_bin, src, tgt]
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        oracle_out = oracle_proc.stdout.strip()

        # Run Agent Script
        agent_cmd = ["bash", agent_script, src, tgt]
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        agent_out = agent_proc.stdout.strip()

        assert agent_proc.returncode == 0, f"Agent script failed on inputs {src} {tgt} with stderr: {agent_proc.stderr}"

        assert oracle_out == agent_out, (
            f"Output mismatch for inputs '{src}' and '{tgt}'.\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output: '{agent_out}'"
        )