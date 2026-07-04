# test_final_state.py
import os
import time
import subprocess
import pandas as pd
import pytest

def test_execution_time_and_output():
    binary_path = "/app/backup-analyzer/target/release/backup-analyzer"
    assert os.path.isfile(binary_path), f"Optimized release binary not found at {binary_path}. Did you run 'cargo build --release'?"

    # Measure execution time
    start_time = time.time()
    result = subprocess.run([binary_path], cwd="/app/backup-analyzer", capture_output=True, text=True)
    end_time = time.time()

    assert result.returncode == 0, f"Binary execution failed with output:\n{result.stderr}\n{result.stdout}"

    execution_time = end_time - start_time
    assert execution_time <= 1.5, f"Execution time was {execution_time:.3f} seconds, which exceeds the threshold of 1.5 seconds."

    # Check output
    anomalies_path = "/home/user/anomalies.csv"
    expected_path = "/app/expected_anomalies.csv"

    assert os.path.isfile(anomalies_path), f"Output file {anomalies_path} is missing."
    assert os.path.isfile(expected_path), f"Expected anomalies file {expected_path} is missing."

    # Compare outputs
    df_actual = pd.read_csv(anomalies_path)
    df_expected = pd.read_csv(expected_path)

    # Ensure required columns are present
    required_columns = ['cluster_id', 'timestamp', 'duration_seconds', 'rolling_avg']
    for col in required_columns:
        assert col in df_actual.columns, f"Column '{col}' is missing from anomalies.csv"

    # Sort both to ensure strict alignment for comparison
    df_actual = df_actual.sort_values(by=['timestamp', 'cluster_id'], ascending=[False, True]).reset_index(drop=True)
    df_expected = df_expected.sort_values(by=['timestamp', 'cluster_id'], ascending=[False, True]).reset_index(drop=True)

    # Compare DataFrames allowing for minor floating point differences in rolling_avg
    try:
        pd.testing.assert_frame_equal(df_actual[required_columns], df_expected[required_columns], check_exact=False, rtol=1e-3)
    except AssertionError as e:
        pytest.fail(f"The generated anomalies.csv does not match the expected output. Details:\n{e}")