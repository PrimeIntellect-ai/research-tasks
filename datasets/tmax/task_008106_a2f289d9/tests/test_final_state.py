# test_final_state.py

import os
import subprocess
import pytest

def test_failing_seed_file():
    path = "/home/user/failing_seed.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you save the failing seed?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "1", f"Expected the first failing seed to be '1', but got '{content}'."

def test_error_trace_log():
    path = "/home/user/error_trace.log"
    assert os.path.isfile(path), f"File {path} does not exist. Did you save the stderr output?"
    with open(path, "r") as f:
        content = f.read()
    assert "Numerical instability detected" in content, "The error trace log does not contain the expected error message 'Numerical instability detected'."

def test_lib_rs_uses_f64():
    path = "/home/user/sim_tracker/src/lib.rs"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "f32" not in content, "Found 'f32' in src/lib.rs. You should change the types to 'f64' to prevent precision loss."
    assert "f64" in content, "Expected to find 'f64' in src/lib.rs to fix the precision loss."

def test_cargo_run_succeeds():
    # Run cargo run -- 1 in the sim_tracker directory
    cwd = "/home/user/sim_tracker"
    assert os.path.isdir(cwd), f"Directory {cwd} does not exist."

    try:
        result = subprocess.run(
            ["cargo", "run", "--", "1"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
    except FileNotFoundError:
        pytest.fail("cargo command not found. Is Rust installed?")
    except subprocess.TimeoutExpired:
        pytest.fail("cargo run timed out.")

    assert result.returncode == 0, f"cargo run failed with exit code {result.returncode}.\nStderr: {result.stderr}\nStdout: {result.stdout}"
    assert "Simulation result:" in result.stdout or "Simulation result:" in result.stderr, "Expected 'Simulation result:' in the output of cargo run."