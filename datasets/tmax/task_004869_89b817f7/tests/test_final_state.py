# test_final_state.py

import os
import hashlib
import pytest

def test_analyzer_modified():
    analyzer_path = '/home/user/network_tools/analyzer.py'
    assert os.path.isfile(analyzer_path), f"File {analyzer_path} does not exist."
    with open(analyzer_path, 'r') as f:
        content = f.read()

    assert "--secret-token" not in content, f"--secret-token argument is still present in {analyzer_path}."
    assert "ANALYZER_TOKEN" in content or "os.environ" in content, f"Environment variable reading logic not found in {analyzer_path}."

def test_analysis_log_exists_and_content():
    log_path = '/home/user/network_tools/analysis.log'
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    expected_content = "TOKEN:SECURE_TOKEN_8842\nDATA_LENGTH:34\n"
    assert content == expected_content, f"Content of {log_path} is incorrect. Expected {repr(expected_content)}, got {repr(content)}."

def test_tls_certs_exist():
    crt_path = '/home/user/network_tools/server.crt'
    key_path = '/home/user/network_tools/server.key'

    assert os.path.isfile(crt_path), f"Certificate file {crt_path} does not exist."
    assert os.path.isfile(key_path), f"Private key file {key_path} does not exist."

def test_transmission_scripts_exist():
    receiver_path = '/home/user/network_tools/secure_receiver.py'
    sender_path = '/home/user/network_tools/secure_sender.py'

    assert os.path.isfile(receiver_path), f"Receiver script {receiver_path} does not exist."
    assert os.path.isfile(sender_path), f"Sender script {sender_path} does not exist."

def test_receipt_txt_content():
    receipt_path = '/home/user/network_tools/receipt.txt'
    assert os.path.isfile(receipt_path), f"File {receipt_path} does not exist."

    expected_log_content = "TOKEN:SECURE_TOKEN_8842\nDATA_LENGTH:34\n"
    expected_hash = hashlib.sha256(expected_log_content.encode('utf-8')).hexdigest()

    with open(receipt_path, 'r') as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Content of {receipt_path} does not match the expected SHA256 digest."