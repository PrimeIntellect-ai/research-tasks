# test_final_state.py
import os
import subprocess
import pytest

def test_decoder_fixed():
    decoder_path = "/home/user/tinyvm/src/decoder.rs"
    assert os.path.isfile(decoder_path), f"{decoder_path} is missing."
    with open(decoder_path, "r") as f:
        content = f.read()

    # Check that uppercase hex support was added
    assert "b'A'..=b'F'" in content, "The logic error in decoder.rs was not fixed. Missing support for uppercase hex characters (b'A'..=b'F')."

def test_cargo_test_passes():
    tinyvm_dir = "/home/user/tinyvm"
    assert os.path.isdir(tinyvm_dir), f"{tinyvm_dir} does not exist."

    # Run cargo test
    result = subprocess.run(["cargo", "test"], cwd=tinyvm_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"'cargo test' failed. Output:\n{result.stdout}\n{result.stderr}"

def test_runner_compiled():
    runner_path = "/home/user/tinyvm/runner"
    assert os.path.isfile(runner_path), f"The compiled executable {runner_path} is missing."
    assert os.access(runner_path, os.X_OK), f"The file {runner_path} is not executable."

def test_result_log():
    log_path = "/home/user/result.log"
    assert os.path.isfile(log_path), f"The result log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert content.strip() == "Result: 50", f"Expected {log_path} to contain 'Result: 50', but got: {content!r}"