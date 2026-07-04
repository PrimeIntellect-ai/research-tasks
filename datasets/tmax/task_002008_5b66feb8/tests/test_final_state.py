# test_final_state.py

import os
import pytest

def test_secret_recovered():
    secret_path = "/home/user/secret.txt"
    assert os.path.isfile(secret_path), f"{secret_path} is missing. Did you write the secret to the correct file?"
    with open(secret_path, "r") as f:
        content = f.read().strip()
    expected_secret = "sk_live_9a8b7c6d5e4f"
    assert content == expected_secret, f"Secret in {secret_path} is incorrect. Expected '{expected_secret}', got '{content}'."

def test_output_parsed():
    output_path = "/home/user/data_pipeline/output.txt"
    assert os.path.isfile(output_path), f"{output_path} is missing. Did you run the compiled parser?"
    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    expected = ["tk_abc12345", "tk_def67890", "tk_ghi11223"]
    assert lines == expected, f"Output in {output_path} is incorrect. It should contain exactly the parsed tokens without extra characters or commas. Expected {expected}, got {lines}."

def test_trace_log():
    trace_path = "/home/user/trace.log"
    assert os.path.isfile(trace_path), f"{trace_path} is missing. Did you modify parser.cpp to append to this file?"
    with open(trace_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    expected = ["Token length: 11", "Token length: 11", "Token length: 11"]
    assert lines == expected, f"Trace log in {trace_path} is incorrect. Expected {expected}, got {lines}."