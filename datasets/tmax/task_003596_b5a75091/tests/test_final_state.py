# test_final_state.py

import os
import sys
import csv
import math
import random
import subprocess
import tempfile
import pytest

def test_libsvm_compiled():
    """Verify that libsvm has been compiled successfully."""
    svm_train_path = "/app/libsvm-3.32/svm-train"
    assert os.path.isfile(svm_train_path), f"Expected executable {svm_train_path} not found. Did you compile libsvm?"
    assert os.access(svm_train_path, os.X_OK), f"File {svm_train_path} is not executable."

def test_run_scale_exists_and_executable():
    """Verify that run_scale.sh exists and is executable."""
    run_scale_path = "/home/user/run_scale.sh"
    assert os.path.isfile(run_scale_path), f"Expected script {run_scale_path} not found."
    assert os.access(run_scale_path, os.X_OK), f"Script {run_scale_path} is not executable."

def test_fuzz_equivalence():
    """Fuzz equivalence test against the oracle."""
    run_scale_path = "/home/user/run_scale.sh"
    oracle_path = "/app/oracle_scale.py"

    assert os.path.isfile(oracle_path), f"Oracle script {oracle_path} not found."

    random.seed(42)
    N = 50

    for i in range(N):
        num_rows = random.randint(5, 100)
        num_cols = random.randint(3, 20)

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f_in:
            input_csv = f_in.name
            writer = csv.writer(f_in)
            for _ in range(num_rows):
                if random.random() < 0.10:
                    # All-zero feature vector
                    row = [0.0] * (num_cols - 1)
                else:
                    row = [random.uniform(-10.0, 10.0) for _ in range(num_cols - 1)]

                label = random.randint(0, 5)
                row.append(label)
                writer.writerow(row)

        agent_out = input_csv + ".agent.txt"
        oracle_out = input_csv + ".oracle.txt"

        try:
            # Run oracle
            subprocess.run([sys.executable, oracle_path, input_csv, oracle_out], check=True, capture_output=True)

            # Run agent
            agent_proc = subprocess.run([run_scale_path, input_csv, agent_out], capture_output=True, text=True)
            assert agent_proc.returncode == 0, f"Agent script failed on input {input_csv}. Stderr: {agent_proc.stderr}"

            assert os.path.isfile(agent_out), f"Agent script did not produce output file {agent_out}"

            with open(oracle_out, 'r') as f_oracle, open(agent_out, 'r') as f_agent:
                oracle_content = f_oracle.read()
                agent_content = f_agent.read()

            assert oracle_content == agent_content, (
                f"Mismatch on run {i+1}!\n"
                f"Input CSV saved at: {input_csv}\n"
                f"Expected output:\n{oracle_content}\n"
                f"Got output:\n{agent_content}"
            )

        finally:
            # Cleanup
            if os.path.exists(input_csv): os.remove(input_csv)
            if os.path.exists(agent_out): os.remove(agent_out)
            if os.path.exists(oracle_out): os.remove(oracle_out)