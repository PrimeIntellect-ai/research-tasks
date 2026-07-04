# test_final_state.py

import os
import time
import subprocess
import pandas as pd
import pytest

def test_fast_aggregator_performance_and_accuracy():
    fast_script = "/home/user/fast_aggregator.py"
    legacy_bin = "/app/legacy_aggregator"
    eval_log = "/tmp/eval_telemetry.log"
    legacy_out = "/tmp/legacy_out.csv"
    fast_out = "/tmp/fast_out.csv"

    assert os.path.exists(fast_script), f"Expected script {fast_script} does not exist."
    assert os.path.exists(legacy_bin), f"Legacy binary {legacy_bin} does not exist."
    assert os.path.exists(eval_log), f"Evaluation log {eval_log} does not exist."

    # Run legacy binary
    start_time = time.time()
    legacy_proc = subprocess.run([legacy_bin, eval_log, legacy_out], capture_output=True)
    legacy_time = time.time() - start_time
    assert legacy_proc.returncode == 0, f"Legacy binary failed with error: {legacy_proc.stderr.decode()}"

    # Run python script
    start_time = time.time()
    fast_proc = subprocess.run(["python3", fast_script, eval_log, fast_out], capture_output=True)
    fast_time = time.time() - start_time
    assert fast_proc.returncode == 0, f"Fast aggregator failed with error: {fast_proc.stderr.decode()}"

    # Verify outputs exist
    assert os.path.exists(legacy_out), "Legacy binary did not produce output CSV."
    assert os.path.exists(fast_out), "Fast aggregator did not produce output CSV."

    # Compare accuracy
    df_legacy = pd.read_csv(legacy_out)
    df_fast = pd.read_csv(fast_out)

    # Check structure
    assert list(df_legacy.columns) == list(df_fast.columns), "Column names or order do not match."
    assert len(df_legacy) == len(df_fast), "Number of rows do not match."

    # Check values
    try:
        pd.testing.assert_frame_equal(df_legacy, df_fast, check_exact=False, atol=1e-4)
        accuracy = 1.0
    except AssertionError as e:
        accuracy = 0.0
        pytest.fail(f"DataFrames do not match: {e}")

    # Calculate speedup
    speedup = legacy_time / fast_time if fast_time > 0 else float('inf')

    assert accuracy == 1.0, "Accuracy is not 1.0 (outputs do not match)."
    assert speedup >= 20.0, f"Speedup is {speedup:.2f}x, which is less than the required 20.0x."