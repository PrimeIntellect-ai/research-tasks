# test_final_state.py
import os
import re
import pytest

def get_secret_coeff():
    memdump_path = "/home/user/memdump.dat"
    if not os.path.exists(memdump_path):
        return None
    with open(memdump_path, "rb") as f:
        content = f.read()
    match = re.search(b"SECRET_COEFF=(\\d+)", content)
    if match:
        return int(match.group(1))
    return None

def get_valid_transactions():
    wal_path = "/home/user/data.wal"
    if not os.path.exists(wal_path):
        return []
    valid_txs = []
    with open(wal_path, "rb") as f:
        for line in f:
            try:
                decoded = line.decode('ascii').strip()
                match = re.match(r"^TX:(\d+)\s+VAL:(\d+)$", decoded)
                if match:
                    valid_txs.append((int(match.group(1)), int(match.group(2))))
            except UnicodeDecodeError:
                pass
    return valid_txs

def test_clean_wal_exists_and_correct():
    clean_wal_path = "/home/user/clean.wal"
    assert os.path.isfile(clean_wal_path), f"File {clean_wal_path} does not exist."

    valid_txs = get_valid_transactions()
    expected_lines = [f"TX:{tx} VAL:{val}" for tx, val in valid_txs]

    with open(clean_wal_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "The contents of clean.wal do not match the expected valid transactions."

def test_executable_exists():
    exe_path = "/home/user/process_math"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_recovered_results_correct():
    results_path = "/home/user/recovered_results.txt"
    assert os.path.isfile(results_path), f"File {results_path} does not exist."

    coeff = get_secret_coeff()
    assert coeff is not None, "Could not find SECRET_COEFF in memdump.dat (test environment issue)."

    valid_txs = get_valid_transactions()
    expected_results = [f"TX:{tx} RESULT:{val * coeff}" for tx, val in valid_txs]

    with open(results_path, "r") as f:
        actual_results = [line.strip() for line in f if line.strip()]

    assert actual_results == expected_results, "The contents of recovered_results.txt do not match the expected computed results."