# test_final_state.py

import os
import stat
import random
import subprocess
import pytest

def test_json2csv_installed():
    bin_path = '/home/user/.local/bin/json2csv'
    assert os.path.isfile(bin_path), f"{bin_path} is missing. Did you install the package?"
    st = os.stat(bin_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{bin_path} is not executable."

def test_artifacts_csv_created():
    csv_path = '/home/user/artifacts.csv'
    assert os.path.isfile(csv_path), f"{csv_path} is missing."
    with open(csv_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 7, "artifacts.csv should have 7 lines (1 header + 6 data rows)."
    assert lines[0] == "artifact_id,run_id,status,latency_ms", "artifacts.csv header is incorrect."
    assert "ART-101,r1,SUCCESS,45" in lines, "artifacts.csv is missing expected data rows."

def test_bayesian_benchmark_script_exists():
    script_path = '/home/user/bayesian_benchmark.sh'
    assert os.path.isfile(script_path), f"{script_path} is missing."

def test_fuzz_equivalence():
    agent_script = '/home/user/bayesian_benchmark.sh'
    oracle_script = '/app/oracle_benchmark.sh'

    assert os.path.isfile(agent_script), f"Agent script {agent_script} not found."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} not found."

    random.seed(42)
    artifacts = ['ART-101', 'ART-102', 'ART-103']

    for _ in range(100):
        art = random.choice(artifacts)
        lat = str(random.randint(10, 150))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_script, art, lat],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, "Oracle script failed"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ['/bin/bash', agent_script, art, lat],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed for input {art} {lat}. Error: {agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch for inputs: artifact_id={art}, latency_threshold={lat}.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )