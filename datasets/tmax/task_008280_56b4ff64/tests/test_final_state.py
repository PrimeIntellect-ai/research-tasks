# test_final_state.py

import os
import pytest

def test_cargo_config_fixed():
    config_path = "/home/user/sim_solver/.cargo/config.toml"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            content = f.read()
        assert "link-arg=-lnonexistent_legacy_math_lib" not in content, "The bad linker flag is still present in .cargo/config.toml"
    else:
        # If deleted, that's also an acceptable way to remove the bad flag
        pass

def test_main_rs_fixed():
    main_rs_path = "/home/user/sim_solver/src/main.rs"
    assert os.path.isfile(main_rs_path), f"{main_rs_path} is missing"

    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "-2.0" in content, "The initial guess in src/main.rs was not updated to -2.0"
    assert "let mut x: f64 = 0.0;" not in content, "The buggy initial guess of 0.0 is still in src/main.rs"

def test_diagnostics_log_contains_correct_output():
    log_path = "/home/user/diagnostics.log"
    assert os.path.isfile(log_path), f"{log_path} is missing. Did you save the output of cargo run?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "Converged root: -1.769292" in content, "The diagnostics.log does not contain the expected convergence output."