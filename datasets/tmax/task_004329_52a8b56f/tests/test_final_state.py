# test_final_state.py

import os
import time
import subprocess
import pandas as pd
from sklearn.metrics import mean_squared_error
import pytest

def test_pipeline_exec_exists():
    exec_path = "/home/user/pipeline_exec"
    assert os.path.isfile(exec_path), f"Executable missing at {exec_path}"
    assert os.access(exec_path, os.X_OK), f"File at {exec_path} is not executable"

def test_pipeline_execution_time_and_output():
    exec_path = "/home/user/pipeline_exec"
    output_path = "/home/user/pagerank_results.csv"

    # Remove output file if it exists to ensure we are generating a new one
    if os.path.exists(output_path):
        os.remove(output_path)

    start_time = time.time()
    result = subprocess.run([exec_path], capture_output=True, text=True)
    end_time = time.time()

    assert result.returncode == 0, f"Execution failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    runtime = end_time - start_time
    assert runtime <= 1.5, f"Execution time {runtime:.4f} seconds exceeds the threshold of 1.5 seconds. The fastgraph library or the C++ pipeline might not be properly optimized."

    assert os.path.isfile(output_path), f"Output file missing at {output_path} after execution"

def test_pagerank_accuracy():
    output_path = "/home/user/pagerank_results.csv"
    golden_path = "/app/golden_pagerank.csv"

    assert os.path.isfile(output_path), f"Output file missing at {output_path}"
    assert os.path.isfile(golden_path), f"Golden reference file missing at {golden_path}"

    try:
        df_out = pd.read_csv(output_path)
    except Exception as e:
        pytest.fail(f"Failed to read output CSV {output_path}: {e}")

    try:
        df_gold = pd.read_csv(golden_path)
    except Exception as e:
        pytest.fail(f"Failed to read golden CSV {golden_path}: {e}")

    assert 'id' in df_out.columns and 'pagerank' in df_out.columns, "Output CSV must contain 'id' and 'pagerank' columns"
    assert 'id' in df_gold.columns and 'pagerank' in df_gold.columns, "Golden CSV must contain 'id' and 'pagerank' columns"

    # Merge on id to ensure we compare the right nodes
    df_merged = pd.merge(df_gold, df_out, on='id', suffixes=('_gold', '_out'))

    assert len(df_merged) == len(df_gold), f"Output is missing some node IDs. Expected {len(df_gold)}, found {len(df_merged)} matching IDs."

    mse = mean_squared_error(df_merged['pagerank_gold'], df_merged['pagerank_out'])

    assert mse <= 1e-5, f"Mean Squared Error of PageRank is {mse:.2e}, which exceeds the threshold of 1e-5."