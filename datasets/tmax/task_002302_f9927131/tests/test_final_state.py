# test_final_state.py
import os
import json
import subprocess
import hashlib
import pytest

def test_new_hash_correctness():
    hash_path = "/home/user/new_hash.txt"
    assert os.path.isfile(hash_path), f"Expected file {hash_path} to exist."

    with open(hash_path, "r") as f:
        actual_hash = f.read().strip()

    expected_string = "old_pwd_MasterSecr3t!_RotateMeNow2024!"
    expected_hash = hashlib.sha256(expected_string.encode()).hexdigest()

    assert actual_hash == expected_hash, f"Hash in {hash_path} is incorrect. Expected exact SHA256 hex digest of the required string."

def test_detect_redirects_f1_score():
    script_path = "/home/user/detect_redirects.py"
    log_path = "/app/hidden_test.log"

    assert os.path.isfile(script_path), f"Expected script {script_path} to exist."
    assert os.path.isfile(log_path), f"Expected log file {log_path} to exist."

    try:
        result = subprocess.run(
            ["python3", script_path, log_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=15
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script {script_path} failed to execute with exit code {e.returncode}. Stderr: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script {script_path} timed out during execution.")

    try:
        predicted_list = json.loads(result.stdout)
        if not isinstance(predicted_list, list):
            pytest.fail("Script output is valid JSON but not an array.")
        predicted = set(predicted_list)
    except json.JSONDecodeError:
        pytest.fail(f"Script output is not valid JSON. Output was: {result.stdout[:100]}...")

    # The hidden truth IPs as defined in the task setup
    truth = {"10.0.0.5", "192.168.1.100", "172.16.0.4"}

    tp = len(predicted & truth)
    fp = len(predicted - truth)
    fn = len(truth - predicted)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.90, f"F1 score {f1:.4f} is below the threshold of 0.90. (Precision: {precision:.4f}, Recall: {recall:.4f})"