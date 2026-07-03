# test_final_state.py

import os
import subprocess
import pytest

def test_agent_binary_exists_and_executable():
    agent_bin = "/home/user/audit"
    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} does not exist. Did you compile your Go code?"
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."

def test_fuzz_equivalence():
    agent_bin = "/home/user/audit"
    oracle_bin = "/app/oracle_audit_bin"
    fuzz_file = "/app/fuzz_pairs.txt"

    assert os.path.isfile(fuzz_file), f"Fuzz pairs file {fuzz_file} is missing."
    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} is missing."

    with open(fuzz_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "Fuzz pairs file is empty."

    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            continue
        source_node, target_node = parts[0], parts[1]

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin, source_node, target_node],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on {source_node} {target_node}:\n{oracle_proc.stderr}"
        oracle_stdout = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            [agent_bin, source_node, target_node],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent failed (exit code {agent_proc.returncode}) on {source_node} {target_node}:\n{agent_proc.stderr}"
        agent_stdout = agent_proc.stdout.strip()

        assert agent_stdout == oracle_stdout, (
            f"Mismatch on inputs: source={source_node}, target={target_node}\n"
            f"Expected (Oracle): {oracle_stdout}\n"
            f"Got (Agent):       {agent_stdout}"
        )