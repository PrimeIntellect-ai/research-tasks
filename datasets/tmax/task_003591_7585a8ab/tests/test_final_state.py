# test_final_state.py

import os
import subprocess
import pytest

def test_c_executable_exists():
    executable = "/home/user/math_ops/math_diff"
    assert os.path.isfile(executable), f"Executable {executable} was not created."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_perf_log():
    log_file = "/home/user/artifacts/perf.log"
    assert os.path.isfile(log_file), f"Performance log {log_file} was not created."
    with open(log_file, "r") as f:
        content = f.read()
    assert "real" in content, f"'real' not found in {log_file}."
    assert "user" in content, f"'user' not found in {log_file}."
    assert "sys" in content, f"'sys' not found in {log_file}."

def test_rust_compiles():
    # Run cargo build to verify it compiles cleanly
    result = subprocess.run(
        ["cargo", "build", "--manifest-path", "/home/user/verifier/Cargo.toml"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"Rust verifier failed to compile:\n{result.stderr.decode('utf-8')}"

def test_diff_contents():
    c_diff = "/home/user/artifacts/c_diff.txt"
    rust_diff = "/home/user/artifacts/rust_diff.txt"

    assert os.path.isfile(c_diff), f"C diff output {c_diff} was not created."
    assert os.path.isfile(rust_diff), f"Rust diff output {rust_diff} was not created."

    with open(c_diff, "r") as f:
        c_lines = f.read().strip().splitlines()

    with open(rust_diff, "r") as f:
        rust_lines = f.read().strip().splitlines()

    assert c_lines == rust_lines, "C diff and Rust diff outputs do not match."

    # Compute expected symmetric difference
    set_a = "/home/user/data/setA.txt"
    set_b = "/home/user/data/setB.txt"

    assert os.path.isfile(set_a), f"Dataset {set_a} is missing."
    assert os.path.isfile(set_b), f"Dataset {set_b} is missing."

    with open(set_a, "r") as f:
        a_vals = set(int(x.strip()) for x in f if x.strip())
    with open(set_b, "r") as f:
        b_vals = set(int(x.strip()) for x in f if x.strip())

    expected_diff = sorted(a_vals.symmetric_difference(b_vals))
    expected_lines = [str(x) for x in expected_diff]

    assert c_lines == expected_lines, f"The output diff does not match the expected symmetric difference."