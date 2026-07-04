# test_final_state.py
import json
import os
import random
import subprocess
import pytest
import numpy as np

def generate_input_data(seed):
    np.random.seed(seed)
    random.seed(seed)

    rows = random.randint(50, 300)
    cols = random.randint(10, 50)

    arr = np.random.randn(rows, cols)

    # Add large outliers to 10% of rows
    num_outliers = max(1, int(0.1 * rows))
    outlier_indices = np.random.choice(rows, num_outliers, replace=False)
    arr[outlier_indices] += 50.0

    # 5% of elements are null
    num_nulls = int(0.05 * rows * cols)
    null_rows = np.random.choice(rows, num_nulls, replace=True)
    null_cols = np.random.choice(cols, num_nulls, replace=True)

    # Convert to list and add nulls
    data = arr.tolist()
    for r, c in zip(null_rows, null_cols):
        data[r][c] = None

    return {"embeddings": data}

def test_pca_fixed():
    pca_file = "/app/pyod-1.0.9/pyod/models/pca.py"
    assert os.path.isfile(pca_file), f"File {pca_file} is missing."
    with open(pca_file, "r") as f:
        content = f.read()
    assert "* 0.0  # PERTURBED" not in content, "The perturbation '* 0.0  # PERTURBED' was not removed from pca.py."

def test_fuzz_equivalence():
    agent_script = "/home/user/process_embeddings.py"
    oracle_script = "/opt/oracle/process_embeddings_oracle.py"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script missing: {oracle_script}"

    for i in range(200):
        input_data = generate_input_data(i)
        input_json = json.dumps(input_data)

        # Run oracle
        oracle_proc = subprocess.run(
            ["python", oracle_script],
            input=input_json,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input seed {i}: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["python", agent_script],
            input=input_json,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input seed {i}:\nSTDERR:\n{agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        if agent_out != oracle_out:
            # Optionally parse JSON to compare structure, but task requires exact match
            try:
                agent_parsed = json.loads(agent_out)
                oracle_parsed = json.loads(oracle_out)
                assert agent_parsed == oracle_parsed, f"JSON output structure mismatch on input seed {i}."
            except json.JSONDecodeError:
                pass

            assert agent_out == oracle_out, f"Bit-exact output mismatch on input seed {i}.\nExpected (Oracle):\n{oracle_out[:200]}...\nActual (Agent):\n{agent_out[:200]}..."