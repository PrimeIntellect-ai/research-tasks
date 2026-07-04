# test_final_state.py
import os
import pytest

def test_anomaly_ip_content():
    path = "/home/user/anomaly_ip.txt"
    assert os.path.isfile(path), f"File {path} is missing. You need to write the anomalous IP address to this file."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "172.16.45.99"
    assert content == expected, f"Incorrect anomaly IP in {path}. Expected '{expected}', but got '{content}'."

def test_missing_symbol_content():
    path = "/home/user/missing_symbol.txt"
    assert os.path.isfile(path), f"File {path} is missing. You need to write the missing function symbol to this file."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "lib_crypto_verify_v2"
    assert content == expected, f"Incorrect missing symbol in {path}. Expected '{expected}', but got '{content}'."

def test_binary_secret_content():
    path = "/home/user/binary_secret.txt"
    assert os.path.isfile(path), f"File {path} is missing. You need to write the extracted password to this file."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "SuperSecretDev0ps_99!"
    assert content == expected, f"Incorrect binary secret in {path}. Expected '{expected}', but got '{content}'."