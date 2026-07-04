# test_final_state.py
import os
import subprocess
import pytest

def test_recovered_secret():
    secret_path = "/home/user/recovered_secret.txt"
    assert os.path.exists(secret_path), f"{secret_path} does not exist."

    with open(secret_path, 'r') as f:
        content = f.read()

    assert content == "vlt_892nf8923nf8923f", "The recovered secret is incorrect or contains extra whitespace/newlines."

def test_yield_result():
    result_path = "/home/user/yield_result.txt"
    assert os.path.exists(result_path), f"{result_path} does not exist."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    # 500000 * (10000 + (450 * 5)) / 10000 = 612500
    assert content == "612500", "The calculated yield result is incorrect."

def test_lib_rs_fixed():
    lib_path = "/home/user/yield-calculator/src/lib.rs"
    assert os.path.exists(lib_path), f"{lib_path} does not exist."

    with open(lib_path, 'r') as f:
        content = f.read()

    # Check that the buggy formula is gone
    assert "(principal * 10000 + rate_bps) * time_years / 10000" not in content, "The buggy formula is still present in src/lib.rs."

    # Run cargo test if possible to ensure it compiles and passes
    repo_path = "/home/user/yield-calculator"
    env = os.environ.copy()
    env["VAULT_SECRET"] = "vlt_892nf8923nf8923f"

    try:
        result = subprocess.run(
            ["cargo", "test"],
            cwd=repo_path,
            env=env,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Cargo tests failed:\n{result.stdout}\n{result.stderr}"
    except FileNotFoundError:
        # If cargo is not installed in the test environment, fallback to a simple string check
        assert "principal * (10000 + (rate_bps * time_years)) / 10000" in content.replace(" ", ""), "The corrected formula was not found in src/lib.rs."