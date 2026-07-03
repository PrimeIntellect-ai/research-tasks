# test_final_state.py
import os
import subprocess
import pytest

def test_run_pipeline_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_rust_compiles():
    rust_dir = "/home/user/rust_analyzer"
    assert os.path.exists(rust_dir), f"{rust_dir} does not exist."
    result = subprocess.run(["cargo", "check"], cwd=rust_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"Rust project failed to compile. Cargo check output:\n{result.stderr}"

def test_payload_bin_exists():
    bin_path = "/home/user/payload.bin"
    assert os.path.exists(bin_path), f"{bin_path} does not exist. Did protoc run successfully?"
    assert os.path.getsize(bin_path) == 15, f"Expected {bin_path} to be exactly 15 bytes."

def test_test_result_log():
    log_path = "/home/user/test_result.log"
    assert os.path.exists(log_path), f"{log_path} does not exist. Did the script redirect output properly?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "First byte: 10" in content, f"Expected 'First byte: 10' in {log_path}, got:\n{content}"
    assert "Total length: 15" in content, f"Expected 'Total length: 15' in {log_path}, got:\n{content}"