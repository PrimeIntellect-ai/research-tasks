# test_final_state.py
import os
import subprocess
import json
import pytest

def test_net_bundle_directory_exists():
    bundle_dir = "/home/user/net_bundle"
    assert os.path.isdir(bundle_dir), f"The directory {bundle_dir} does not exist. Did your script create it?"

def test_oracle_accuracy():
    bundle_dir = "/home/user/net_bundle"
    oracle_path = "/app/net_oracle"

    assert os.path.exists(oracle_path), f"Oracle binary missing at {oracle_path}."
    assert os.path.isdir(bundle_dir), f"Bundle directory missing at {bundle_dir}."

    try:
        result = subprocess.run(
            [oracle_path, bundle_dir],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle binary execution failed with return code {e.returncode}. stderr: {e.stderr}")
    except Exception as e:
        pytest.fail(f"Failed to execute oracle binary: {e}")

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON output from oracle binary. Output was: {result.stdout}")

    assert "accuracy" in data, f"Oracle JSON output missing 'accuracy' key. Output: {data}"

    accuracy = float(data["accuracy"])
    threshold = 0.95

    assert accuracy >= threshold, (
        f"Accuracy metric too low. "
        f"Expected accuracy >= {threshold}, but got {accuracy}. "
        f"Ensure your authorized_keys, fstab_snippet, and group_snippet are correctly formatted and contain the right data."
    )