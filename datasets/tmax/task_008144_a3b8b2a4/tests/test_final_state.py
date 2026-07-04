# test_final_state.py

import os
import subprocess
import pytest

def test_success_log():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"Expected {log_path} to exist."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert "ALL_TESTS_PASSED" in content, f"Expected {log_path} to contain 'ALL_TESTS_PASSED'."

def test_rust_binary_exists_and_executable():
    bin_path = "/home/user/rust_calc/target/debug/rust_calc"
    assert os.path.isfile(bin_path), f"Expected compiled Rust binary at {bin_path}."
    assert os.access(bin_path, os.X_OK), f"Expected {bin_path} to be executable."

def test_rust_binary_behavior():
    bin_path = "/home/user/rust_calc/target/debug/rust_calc"

    # Test op_id = 1, input = 10 -> expected 52
    try:
        result1 = subprocess.run([bin_path, "1", "10"], capture_output=True, text=True, timeout=5)
        assert result1.returncode == 0, "Rust binary exited with non-zero status for op 1."
        assert result1.stdout.strip() == "52", f"Expected output '52' for op 1 input 10, got '{result1.stdout.strip()}'."
    except subprocess.TimeoutExpired:
        pytest.fail("Rust binary timed out. Is the mock server missing or hanging?")

    # Test op_id = 2, input = 20 -> expected 5
    try:
        result2 = subprocess.run([bin_path, "2", "20"], capture_output=True, text=True, timeout=5)
        assert result2.returncode == 0, "Rust binary exited with non-zero status for op 2."
        assert result2.stdout.strip() == "5", f"Expected output '5' for op 2 input 20, got '{result2.stdout.strip()}'."
    except subprocess.TimeoutExpired:
        pytest.fail("Rust binary timed out. Is the mock server missing or hanging?")

def test_encoded_ops_generated_correctly():
    file_path = "/home/user/rust_calc/src/encoded_ops.rs"
    assert os.path.isfile(file_path), f"Expected generated file at {file_path}."

    with open(file_path, "r") as f:
        content = f.read()

    # Check for the required function signature
    assert "pub fn apply_op" in content, "Missing 'pub fn apply_op' in generated Rust file."
    assert "match" in content, "Missing 'match' statement in generated Rust file."

    # Check if the logic for op 1 (+42) and op 2 (-15) are present
    # We won't strictly match the exact Rust syntax but ensure the numbers and logic are there
    assert "42" in content, "Missing constant 42 in generated Rust file."
    assert "15" in content, "Missing constant 15 in generated Rust file."