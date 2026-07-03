# test_final_state.py

import os
import subprocess
import pytest

def test_legacy_c_moved():
    old_path = "/home/user/legacy.c"
    new_path = "/home/user/math_eval/legacy/legacy.c"

    assert not os.path.exists(old_path), f"Legacy file still exists at {old_path}, it should have been moved."
    assert os.path.isfile(new_path), f"Legacy file not found at {new_path}."

def test_rust_project_initialized():
    cargo_toml = "/home/user/math_eval/evaluator/Cargo.toml"
    main_rs = "/home/user/math_eval/evaluator/src/main.rs"

    assert os.path.isfile(cargo_toml), f"Rust project Cargo.toml not found at {cargo_toml}."
    assert os.path.isfile(main_rs), f"Rust main.rs not found at {main_rs}."

def test_rust_binary_behavior():
    project_dir = "/home/user/math_eval/evaluator"

    # Compile the Rust project in release mode
    build_result = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert build_result.returncode == 0, f"Rust project failed to compile:\n{build_result.stderr}"

    binary_path = os.path.join(project_dir, "target/release/evaluator")
    assert os.path.isfile(binary_path), "Compiled binary not found in target/release/evaluator."

    # Test valid expression
    valid_run = subprocess.run(
        [binary_path, "add(10, 5)"],
        capture_output=True,
        text=True
    )
    assert valid_run.returncode == 0, "Binary failed on valid input."
    assert valid_run.stdout.strip() == "15", f"Expected '15', got '{valid_run.stdout.strip()}'"

    # Test division by zero
    div_zero_run = subprocess.run(
        [binary_path, "div(10, 0)"],
        capture_output=True,
        text=True
    )
    assert div_zero_run.returncode == 0, "Binary must exit with code 0 on division by zero."
    assert div_zero_run.stdout.strip() == "EVAL_ERROR", f"Expected 'EVAL_ERROR' on div by zero, got '{div_zero_run.stdout.strip()}'"

    # Test malformed input
    malformed_run = subprocess.run(
        [binary_path, "add(10, )"],
        capture_output=True,
        text=True
    )
    assert malformed_run.returncode == 0, "Binary must exit with code 0 on malformed input."
    assert malformed_run.stdout.strip() == "EVAL_ERROR", f"Expected 'EVAL_ERROR' on malformed input, got '{malformed_run.stdout.strip()}'"

def test_benchmark_result():
    result_file = "/home/user/benchmark_result.txt"
    expected_file = "/tmp/expected_sum.txt"

    assert os.path.isfile(result_file), f"Benchmark result file not found at {result_file}."
    assert os.path.isfile(expected_file), f"Expected sum file not found at {expected_file}."

    with open(result_file, "r") as f:
        actual_sum = f.read().strip()

    with open(expected_file, "r") as f:
        expected_sum = f.read().strip()

    assert actual_sum == expected_sum, f"Benchmark result sum is incorrect. Expected {expected_sum}, got {actual_sum}."