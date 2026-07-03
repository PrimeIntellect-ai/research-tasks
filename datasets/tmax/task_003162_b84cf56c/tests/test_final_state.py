# test_final_state.py
import os

def test_attacker_ip_correct():
    path = '/home/user/attacker_ip.txt'
    assert os.path.isfile(path), f"File not found: {path}. You must write the attacker's IP to this file."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_ip = '10.55.201.77'
    assert content == expected_ip, f"Incorrect IP in {path}. Expected '{expected_ip}', but got '{content}'."

def test_recovered_wal_data_correct():
    path = '/home/user/recovered.txt'
    assert os.path.isfile(path), f"File not found: {path}. You must write the recovered WAL entries to this file."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "config_host=db.internal.net",
        "max_connections=1024",
        "timeout_ms=5000"
    ]

    assert lines == expected_lines, (
        f"Incorrect recovered data in {path}.\n"
        f"Expected:\n{expected_lines}\n"
        f"Got:\n{lines}\n"
        "Make sure you are skipping non-SET operations (opcode != 1) and correctly handling corrupted/partial records at the end."
    )