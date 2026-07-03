# test_final_state.py

import os
import subprocess
import random
import pytest

def test_awk_stat_fixed_and_built():
    bin_path = "/app/awk-stat-1.1/bin/awk-stat"
    assert os.path.exists(bin_path), f"Executable {bin_path} not found. Did you fix the Makefile and run make?"
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_feature_pipeline_exists_and_executable():
    script_path = "/home/user/feature_pipeline.sh"
    assert os.path.exists(script_path), f"Script {script_path} not found."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def generate_random_csv(filepath, num_rows):
    with open(filepath, 'w') as f:
        f.write("ID,Label,F1,F2,F3,F4,F5\n")
        ids = random.sample(range(1, 1001), num_rows)
        labels = ['A', 'B', 'C', 'D', 'E']
        for i in range(num_rows):
            row = [
                str(ids[i]),
                random.choice(labels),
                str(random.randint(0, 1000)),
                str(random.randint(0, 1000)),
                str(random.randint(0, 1000)),
                str(random.randint(0, 1000)),
                str(random.randint(0, 1000))
            ]
            f.write(",".join(row) + "\n")

def test_fuzz_equivalence(tmp_path):
    oracle_script = "/opt/oracle/reference_pipeline.sh"
    agent_script = "/home/user/feature_pipeline.sh"

    random.seed(42)

    for i in range(50):
        num_rows = random.randint(10, 100)
        csv_path = tmp_path / f"input_{i}.csv"
        generate_random_csv(csv_path, num_rows)

        oracle_proc = subprocess.run([oracle_script, str(csv_path)], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_script, str(csv_path)], capture_output=True, text=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on {csv_path}. Stderr: {oracle_proc.stderr}"
        assert agent_proc.returncode == 0, f"Agent script failed on {csv_path}. Stderr: {agent_proc.stderr}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            with open(csv_path, 'r') as f:
                input_data = f.read()
            pytest.fail(
                f"Output mismatch on random input {i}.\n\n"
                f"Input CSV:\n{input_data}\n"
                f"Expected Output (Oracle):\n{oracle_out}\n\n"
                f"Actual Output (Agent):\n{agent_out}\n"
            )