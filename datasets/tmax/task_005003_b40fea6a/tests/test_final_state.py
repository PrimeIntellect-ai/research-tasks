# test_final_state.py

import os
import subprocess
import random
import csv
import pytest

def test_executable_exists_and_is_executable():
    path = "/home/user/graph_query"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you move it to the correct location?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_fuzz_equivalence():
    agent_exe = "/home/user/graph_query"
    oracle_exe = "/usr/local/bin/oracle_graph_query"

    assert os.path.isfile(oracle_exe), f"Oracle executable {oracle_exe} missing."

    csv_path = "/app/csv-graph-toolkit/edges.csv"
    assert os.path.isfile(csv_path), f"CSV file {csv_path} missing."

    source_ids = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header:
            try:
                source_idx = header.index("source_id")
            except ValueError:
                source_idx = 0
            for row in reader:
                if len(row) > source_idx:
                    source_ids.append(row[source_idx])

    assert source_ids, "No source_ids found in edges.csv"

    # Remove duplicates to ensure diverse testing
    source_ids = list(set(source_ids))

    random.seed(42)
    num_tests = min(50, len(source_ids))
    test_inputs = random.sample(source_ids, num_tests)

    cwd = "/app/csv-graph-toolkit"

    for inp in test_inputs:
        oracle_proc = subprocess.run([oracle_exe, inp], cwd=cwd, capture_output=True, text=True)
        agent_proc = subprocess.run([agent_exe, inp], cwd=cwd, capture_output=True, text=True)

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch for input '{inp}'. "
            f"Oracle returned {oracle_proc.returncode}, Agent returned {agent_proc.returncode}.\n"
            f"Oracle stderr: {oracle_proc.stderr}\n"
            f"Agent stderr: {agent_proc.stderr}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch for input '{inp}'.\n"
            f"Oracle output:\n{oracle_proc.stdout}\n"
            f"Agent output:\n{agent_proc.stdout}"
        )