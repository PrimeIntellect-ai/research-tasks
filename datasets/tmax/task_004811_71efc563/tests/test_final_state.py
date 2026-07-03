# test_final_state.py

import os
import subprocess
import pytest

def test_final_report_exists_and_correct():
    report_path = "/home/user/sec_logger/final_report.txt"
    assert os.path.exists(report_path), f"Final report missing at {report_path}"

    with open(report_path, "r") as f:
        content = f.read()

    expected = "Detected 3 SQLi attempts\n"
    assert content == expected, f"Expected final report to contain exactly {repr(expected)}, but got {repr(content)}"

def test_cargo_toml_configuration():
    cargo_toml_path = "/home/user/sec_logger/rust_lib/Cargo.toml"
    assert os.path.exists(cargo_toml_path), f"Cargo.toml missing at {cargo_toml_path}"

    with open(cargo_toml_path, "r") as f:
        content = f.read()

    # Check for staticlib
    assert "staticlib" in content, "Cargo.toml does not define crate-type containing 'staticlib'"

    # Check for proptest
    assert "proptest" in content, "Cargo.toml does not contain 'proptest' dependency"

def test_ci_build_script():
    script_path = "/home/user/sec_logger/ci_build.sh"
    assert os.path.exists(script_path), f"CI script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"CI script at {script_path} is not executable"

    # Run the script to ensure it completes successfully
    result = subprocess.run(
        [script_path],
        cwd="/home/user/sec_logger",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"CI script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_cargo_test_passes():
    rust_dir = "/home/user/sec_logger/rust_lib"
    assert os.path.isdir(rust_dir), f"Rust library directory missing at {rust_dir}"

    result = subprocess.run(
        ["cargo", "test"],
        cwd=rust_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"cargo test failed.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert "test result: ok" in result.stdout, "cargo test output did not indicate successful test results"
    assert "0 passed" not in result.stdout, "cargo test ran but no tests passed (expected at least one proptest)"