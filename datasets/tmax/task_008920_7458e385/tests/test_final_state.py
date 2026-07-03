# test_final_state.py

import os
import subprocess
import pytest

def test_rust_code_fixed_and_test_added():
    lib_rs_path = "/home/user/app/src/lib.rs"
    assert os.path.exists(lib_rs_path), f"File {lib_rs_path} does not exist."
    with open(lib_rs_path, "r") as f:
        content = f.read()

    # Check if the regression test is present
    assert "test_process_data_regression" in content, "The required test 'test_process_data_regression' is missing in src/lib.rs."

def test_test_output_file():
    output_path = "/home/user/test_output.txt"
    assert os.path.exists(output_path), f"File {output_path} does not exist. Did you redirect the output of cargo test?"
    with open(output_path, "r") as f:
        content = f.read()

    assert "test_process_data_regression" in content, "The test output file does not mention 'test_process_data_regression'."
    assert "ok" in content, "The test output file does not indicate that tests passed (missing 'ok')."

def test_cargo_test_success():
    # Verify that the project actually compiles and tests pass when the correct environment is set
    env = os.environ.copy()
    env["PKG_CONFIG_PATH"] = "/home/user/custom_lib/pkgconfig"

    result = subprocess.run(
        ["cargo", "test"],
        cwd="/home/user/app",
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed. The borrow checker error might not be fixed correctly, or the test failed. Output:\n{result.stdout}\n{result.stderr}"

    # Cargo test output can go to stdout or stderr depending on the version and flags
    combined_output = result.stdout + "\n" + result.stderr
    assert "test_process_data_regression" in combined_output, "The test 'test_process_data_regression' was not executed by cargo test."