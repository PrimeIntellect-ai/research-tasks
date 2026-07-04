# test_final_state.py

import os
import re
import pytest

def compute_f1(pred_file, truth_file):
    with open(pred_file, 'r') as f:
        preds = set([line.strip() for line in f.readlines() if line.strip()])
    with open(truth_file, 'r') as f:
        truths = set([line.strip() for line in f.readlines() if line.strip()])

    tp = len(preds.intersection(truths))
    fp = len(preds - truths)
    fn = len(truths - preds)

    if tp == 0: return 0.0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return 2 * (precision * recall) / (precision + recall)

def test_token_extraction_f1_score():
    pred_file = '/app/compromised_tokens.txt'
    truth_file = '/app/.hidden_truth.txt'

    assert os.path.isfile(pred_file), f"Prediction file {pred_file} is missing."
    assert os.path.isfile(truth_file), f"Truth file {truth_file} is missing."

    f1 = compute_f1(pred_file, truth_file)
    threshold = 0.95
    assert f1 >= threshold, f"F1 Score {f1:.4f} is below the threshold of {threshold}."

def test_ssh_hardening_password_disabled():
    sshd_config_path = '/app/sshd_config'
    assert os.path.isfile(sshd_config_path), f"{sshd_config_path} is missing."

    with open(sshd_config_path, 'r') as f:
        content = f.read()

    # Check that PasswordAuthentication yes is removed or commented out, and no is active
    # A simple check: "PasswordAuthentication no" should be present and uncommented
    lines = [line.strip() for line in content.splitlines()]
    active_lines = [line for line in lines if not line.startswith('#') and line]

    password_auth_directives = [line for line in active_lines if line.startswith('PasswordAuthentication')]

    assert len(password_auth_directives) > 0, "PasswordAuthentication directive missing in active config."
    assert all('no' in line for line in password_auth_directives), "PasswordAuthentication is not set to 'no'."

def test_ssh_hardening_key_generated_and_authorized():
    priv_key_path = '/home/user/.ssh/admin_key'
    pub_key_path = '/home/user/.ssh/admin_key.pub'
    auth_keys_path = '/home/user/.ssh/authorized_keys'

    assert os.path.isfile(priv_key_path), f"Private key {priv_key_path} is missing."
    assert os.path.isfile(pub_key_path), f"Public key {pub_key_path} is missing."
    assert os.path.isfile(auth_keys_path), f"Authorized keys file {auth_keys_path} is missing."

    with open(pub_key_path, 'r') as f:
        pub_key_content = f.read().strip()

    with open(auth_keys_path, 'r') as f:
        auth_keys_content = f.read()

    # The public key should be in the authorized_keys file
    # We can check if the key part (excluding comments) is present
    pub_key_parts = pub_key_content.split()
    if len(pub_key_parts) >= 2:
        key_body = pub_key_parts[1]
        assert key_body in auth_keys_content, "The generated admin_key is not in authorized_keys."
    else:
        assert pub_key_content in auth_keys_content, "The generated admin_key is not in authorized_keys."

def test_architecture_remediation_no_token_args():
    api_path = '/app/api.py'
    worker_path = '/app/worker.py'

    assert os.path.isfile(api_path), f"{api_path} is missing."
    assert os.path.isfile(worker_path), f"{worker_path} is missing."

    with open(api_path, 'r') as f:
        api_content = f.read()

    with open(worker_path, 'r') as f:
        worker_content = f.read()

    assert '--token' not in api_content, f"--token argument is still present in {api_path}."
    assert '--token' not in worker_content, f"--token argument is still present in {worker_path}."

def test_architecture_remediation_redis_usage():
    api_path = '/app/api.py'
    worker_path = '/app/worker.py'

    with open(api_path, 'r') as f:
        api_content = f.read().lower()

    with open(worker_path, 'r') as f:
        worker_content = f.read().lower()

    # Check for redis usage in both files
    assert 'redis' in api_content, f"Redis is not being used in {api_path}."
    assert 'redis' in worker_content, f"Redis is not being used in {worker_path}."

    # Check for the specific list name
    assert 'auth_tasks' in api_content, f"'auth_tasks' list not referenced in {api_path}."
    assert 'auth_tasks' in worker_content, f"'auth_tasks' list not referenced in {worker_path}."