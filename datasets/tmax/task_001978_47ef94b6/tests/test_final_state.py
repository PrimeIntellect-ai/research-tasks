# test_final_state.py
import os
import subprocess
import pandas as pd
import numpy as np
import pytest

def test_engine_executable_exists():
    engine_path = "/home/user/math_engine_repo/build/engine"
    assert os.path.exists(engine_path), f"Compiled engine not found at {engine_path}"
    assert os.path.isfile(engine_path), f"{engine_path} is not a file"
    assert os.access(engine_path, os.X_OK), f"{engine_path} is not executable"

def test_final_output_mse():
    output_path = "/home/user/math_engine_repo/final_output.csv"
    input_path = "/home/user/math_engine_repo/test_queries.csv"
    oracle_path = "/app/oracle_engine"
    oracle_output_path = "/tmp/oracle_output.csv"

    assert os.path.exists(output_path), f"Final output not found at {output_path}"
    assert os.path.exists(input_path), f"Input file not found at {input_path}"
    assert os.path.exists(oracle_path), f"Oracle engine not found at {oracle_path}"

    # Run oracle
    result = subprocess.run([oracle_path, input_path, oracle_output_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Oracle engine failed to run: {result.stderr}"
    assert os.path.exists(oracle_output_path), f"Oracle output not generated at {oracle_output_path}"

    try:
        df_agent = pd.read_csv(output_path, header=None, names=['id', 'val'])
    except Exception as e:
        pytest.fail(f"Failed to read agent output CSV {output_path}: {e}")

    try:
        df_oracle = pd.read_csv(oracle_output_path, header=None, names=['id', 'val'])
    except Exception as e:
        pytest.fail(f"Failed to read oracle output CSV {oracle_output_path}: {e}")

    assert len(df_agent) == len(df_oracle), f"Output rows count mismatch: agent has {len(df_agent)}, oracle has {len(df_oracle)}"

    mse = np.mean((df_agent['val'] - df_oracle['val'])**2)
    threshold = 1e-5

    assert mse <= threshold, f"MSE {mse} exceeds threshold {threshold}"