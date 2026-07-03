# test_final_state.py

import os
import pytest

def test_encoder_executable_exists():
    encoder_path = "/home/user/ci-tools/c-encoder/encoder"
    assert os.path.exists(encoder_path), f"File {encoder_path} does not exist. Did you fix the Makefile and run make?"
    assert os.access(encoder_path, os.X_OK), f"File {encoder_path} is not executable."

def test_test_results_log():
    log_path = "/home/user/ci-tools/test_results.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist. Did you run the Go tests and save the output?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "PASS" in content, f"Expected 'PASS' in {log_path}, but it was not found. The tests might have failed."

def test_go_verifier_implementation():
    test_path = "/home/user/ci-tools/go-verifier/verifier_test.go"
    assert os.path.exists(test_path), f"File {test_path} is missing."

    with open(test_path, "r") as f:
        content = f.read()

    assert "encoding/hex" in content, "The Go test does not import 'encoding/hex'. You must decode the hex output."
    assert "chan " in content or "chan\t" in content or "make(chan" in content, "The Go test does not seem to use channels ('chan')."
    assert "go func" in content or "go " in content, "The Go test does not seem to spawn goroutines ('go func')."