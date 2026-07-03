# test_final_state.py
import json
import os
import stat
import hmac
import hashlib
import pytest

def test_key_permissions():
    """Test that the master_secret.key file has exactly 0400 permissions."""
    key_path = "/app/master_secret.key"
    assert os.path.exists(key_path), f"File {key_path} does not exist."
    st = os.stat(key_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Permissions for {key_path} are {oct(perms)}, expected 0o400."

def test_metric_f1_accuracy():
    """Test that the generated rotated credentials achieve an F1 score >= 0.85."""
    output_path = "/home/user/rotated_credentials.json"
    key_path = "/app/master_secret.key"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.exists(key_path), f"Key file {key_path} does not exist."

    with open(key_path, "rb") as f:
        secret = f.read()

    try:
        with open(output_path, "r") as f:
            generated = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to parse {output_path} as JSON: {e}")

    ground_truth_uids = {"admin_992", "user_103", "service_db_44", "sys_ops_01"}

    correct_matches = 0
    for uid in ground_truth_uids:
        if uid in generated:
            expected_sig = hmac.new(secret, uid.encode('utf-8'), hashlib.sha256).hexdigest()
            expected_token = f"{uid}.{expected_sig}"
            if generated[uid] == expected_token:
                correct_matches += 1

    precision = correct_matches / max(len(generated), 1)
    recall = correct_matches / len(ground_truth_uids)

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.85, f"F1 accuracy {f1:.3f} is below the threshold of 0.85. Correct matches: {correct_matches}, Generated count: {len(generated)}"