# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/accel_lib"

def test_cargo_test_native():
    """Ensure cargo test passes on the native host."""
    result = subprocess.run(
        ["cargo", "test"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'cargo test' failed on native host:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_cargo_check_riscv():
    """Ensure cargo check passes for riscv64gc-unknown-none-elf."""
    result = subprocess.run(
        ["cargo", "check", "--target", "riscv64gc-unknown-none-elf"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'cargo check' failed for riscv64gc-unknown-none-elf:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_cargo_check_riscv_fast_math_fails():
    """Ensure cargo check fails with the exact panic message when fast_math is enabled on riscv."""
    result = subprocess.run(
        ["cargo", "check", "--target", "riscv64gc-unknown-none-elf", "--features", "fast_math"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode != 0, "Expected 'cargo check' to fail with fast_math on riscv64, but it succeeded."

    expected_panic_msg = "Constraint violation: fast_math requires x86_64 or aarch64"
    assert expected_panic_msg in result.stderr, (
        f"Expected panic message '{expected_panic_msg}' not found in stderr.\n"
        f"Actual STDERR:\n{result.stderr}"
    )