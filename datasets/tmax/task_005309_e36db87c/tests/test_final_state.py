# test_final_state.py

import os
import pytest

def test_rust_project_exists():
    assert os.path.isfile("/home/user/mcmc_stat/Cargo.toml"), "Cargo.toml is missing. Rust project not created properly."
    assert os.path.isfile("/home/user/mcmc_stat/src/lib.rs"), "src/lib.rs is missing."

def test_run_test_script_exists_and_executable():
    script_path = "/home/user/run_test.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_test_results_generated():
    results_path = "/home/user/test_results.txt"
    assert os.path.isfile(results_path), f"{results_path} is missing. Did the script run?"

    with open(results_path, "r") as f:
        content = f.read()

    assert "test_mcmc_analytical_validation" in content, "The test 'test_mcmc_analytical_validation' was not found in the test results."
    assert "test result: ok" in content or "ok" in content.split("test_mcmc_analytical_validation")[1].split("\n")[0], "The Rust test did not pass according to test_results.txt."

def test_cargo_toml_dependencies():
    with open("/home/user/mcmc_stat/Cargo.toml", "r") as f:
        content = f.read()
    assert "rand" in content, "The 'rand' crate is missing from Cargo.toml"
    assert "rand_distr" in content, "The 'rand_distr' crate is missing from Cargo.toml"