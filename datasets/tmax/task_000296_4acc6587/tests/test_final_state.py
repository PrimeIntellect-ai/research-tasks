# test_final_state.py

import os
import pytest

def test_corrupted_seq_log():
    log_path = "/home/user/corrupted_seq.log"
    assert os.path.isfile(log_path), f"Expected file {log_path} is missing. Did you handle corrupted inputs and write to the log?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_seqs = ["4", "7"]
    assert lines == expected_seqs, f"Content of {log_path} is incorrect. Expected {expected_seqs}, got {lines}."

def test_results_log():
    log_path = "/home/user/results.log"
    assert os.path.isfile(log_path), f"Expected file {log_path} is missing. Did you write the results to this file?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_dict = {
        "AAPL": 10000000.5,
        "MSFT": 500.0,
        "TSLA": 120.5
    }

    actual_dict = {}
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            sym = parts[0].strip()
            try:
                val = float(parts[1].strip())
                actual_dict[sym] = val
            except ValueError:
                pass

    for sym, expected_val in expected_dict.items():
        assert sym in actual_dict, f"Symbol {sym} missing from {log_path}."
        assert actual_dict[sym] == expected_val, f"Precision loss or incorrect sum for {sym}. Expected {expected_val}, got {actual_dict[sym]}."

def test_compiled_binary():
    bin_path = "/home/user/trade_aggregator"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing. Did you compile the program?"
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."