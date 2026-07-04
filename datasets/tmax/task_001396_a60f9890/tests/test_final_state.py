# test_final_state.py

import os
import subprocess
import pytest

def test_cargo_test_log_exists_and_passed():
    """Verify that cargo_test.log was created and shows the property test passed."""
    log_path = "/home/user/cargo_test.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you redirect cargo test output?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "test_evaluate_rule_properties" in content, "The proptest 'test_evaluate_rule_properties' was not found in cargo_test.log."

    # Check for general test success indicators
    assert "ok" in content or "passed" in content, "cargo_test.log does not indicate successful test execution."

def test_runner_output_log_correct():
    """Verify that runner_output.log contains the correct results from the C program."""
    log_path = "/home/user/runner_output.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you run the executable and redirect output?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "Res1: 1" in content, "runner_output.log is missing 'Res1: 1' (Expected rule MAX:10 with 5 reqs to be allowed)."
    assert "Res2: 0" in content, "runner_output.log is missing 'Res2: 0' (Expected rule MAX:10 with 15 reqs to be denied)."
    assert "Res3: -1" in content, "runner_output.log is missing 'Res3: -1' (Expected INVALID rule to return error)."

def test_runner_executable_exists_and_linked():
    """Verify that the runner executable is built and dynamically linked to librate_eval.so."""
    runner_path = "/home/user/project/build/runner"
    assert os.path.isfile(runner_path), f"{runner_path} does not exist. Did you run cmake and make?"
    assert os.access(runner_path, os.X_OK), f"{runner_path} is not executable."

    try:
        ldd_output = subprocess.check_output(["ldd", runner_path], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run ldd on {runner_path}: {e.output}")

    assert "librate_eval.so" in ldd_output, "runner is not dynamically linked against librate_eval.so."

def test_proptest_dependency_added():
    """Verify that proptest was added to Cargo.toml."""
    cargo_toml_path = "/home/user/project/rust_lib/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), f"{cargo_toml_path} does not exist."

    with open(cargo_toml_path, "r") as f:
        content = f.read()

    assert "proptest" in content, "proptest crate was not found in Cargo.toml."