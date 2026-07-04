# test_final_state.py

import os
import subprocess
import pandas as pd
import pytest

def test_policy_engine_exists_and_executable():
    """Ensure the compiled C program exists and is executable."""
    binary_path = "/home/user/policy_engine"
    assert os.path.isfile(binary_path), f"Binary not found at {binary_path}. Did you compile your C program?"
    assert os.access(binary_path, os.X_OK), f"File at {binary_path} is not executable."

def test_policy_engine_accuracy():
    """Run the policy engine against the hidden test set and verify classification accuracy."""
    binary_path = "/home/user/policy_engine"
    hidden_test_json = "/app/hidden_test_audit.json"
    hidden_expected_csv = "/app/hidden_expected.csv"

    assert os.path.isfile(hidden_test_json), f"Hidden test JSON is missing: {hidden_test_json}"
    assert os.path.isfile(hidden_expected_csv), f"Hidden expected CSV is missing: {hidden_expected_csv}"

    cmd = [binary_path, hidden_test_json]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail("The policy engine binary timed out after 10 seconds.")
    except Exception as e:
        pytest.fail(f"Failed to run binary: {e}")

    assert result.returncode == 0, f"Binary exited with non-zero return code: {result.returncode}\nStderr: {result.stderr}"

    output_csv_path = "/tmp/agent_output.csv"
    with open(output_csv_path, "w") as f:
        f.write(result.stdout.strip())

    try:
        df_agent = pd.read_csv(output_csv_path)
    except Exception as e:
        pytest.fail(f"Failed to parse agent output as CSV: {e}\nOutput snippet:\n{result.stdout[:500]}")

    try:
        df_truth = pd.read_csv(hidden_expected_csv)
    except Exception as e:
        pytest.fail(f"Failed to read hidden expected CSV: {e}")

    assert len(df_agent) == len(df_truth), f"Row count mismatch. Expected {len(df_truth)}, got {len(df_agent)}."
    assert "id" in df_agent.columns, "Agent output CSV must contain an 'id' column."
    assert "is_vulnerable" in df_agent.columns, "Agent output CSV must contain an 'is_vulnerable' column."

    merged = pd.merge(df_truth, df_agent, on="id", suffixes=('_true', '_pred'))

    assert len(merged) == len(df_truth), "Mismatch in 'id' values between expected and actual outputs."

    correct = (merged['is_vulnerable_true'] == merged['is_vulnerable_pred']).sum()
    accuracy = correct / len(df_truth)

    assert accuracy >= 1.0, f"Classification accuracy is {accuracy:.4f}, expected >= 1.0. Your policy engine incorrectly classified some events."