# test_final_state.py
import os
import time
import subprocess
import pandas as pd
import pytest

def test_query_results_mae():
    student_file = "/home/user/query_results.csv"
    golden_file = "/tmp/golden_results.csv"

    assert os.path.isfile(student_file), f"Student output file {student_file} does not exist."
    assert os.path.isfile(golden_file), f"Golden reference file {golden_file} does not exist."

    # Read both files
    try:
        student_df = pd.read_csv(student_file, header=None, names=["Source", "Target", "Distance"])
    except Exception as e:
        pytest.fail(f"Failed to read {student_file}: {e}")

    try:
        golden_df = pd.read_csv(golden_file, header=None, names=["Source", "Target", "Distance"])
    except Exception as e:
        pytest.fail(f"Failed to read {golden_file}: {e}")

    assert len(student_df) == len(golden_df), f"Expected {len(golden_df)} rows, but got {len(student_df)} rows in {student_file}."

    # Merge on Source and Target to ensure we compare the right pairs
    merged = pd.merge(golden_df, student_df, on=["Source", "Target"], suffixes=('_golden', '_student'))
    assert len(merged) == len(golden_df), "Mismatch in Source/Target pairs between student and golden results."

    # Compute MAE
    mae = (merged['Distance_golden'] - merged['Distance_student']).abs().mean()

    assert mae <= 0.0, f"MAE is {mae}, expected 0.0. The distances are incorrect."

def test_binary_execution_time():
    binary_path = "/app/kg-path-finder-0.9/kg-path-finder"
    network_file = "/home/user/bio_network.tsv"
    queries_file = "/home/user/protein_queries.tsv"

    assert os.path.isfile(binary_path), f"Binary {binary_path} not found. Did you recompile?"

    # Run the binary and measure time
    start_time = time.time()
    try:
        process = subprocess.run(
            [binary_path, network_file, queries_file],
            capture_output=True,
            timeout=5.0
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Execution timed out after 5 seconds. The program is still too slow.")

    end_time = time.time()
    execution_time = end_time - start_time

    assert process.returncode == 0, f"Binary execution failed with return code {process.returncode}."
    assert execution_time <= 0.5, f"Execution time was {execution_time:.3f}s, expected <= 0.5s. Did you optimize the Makefile?"