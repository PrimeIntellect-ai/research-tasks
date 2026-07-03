# test_final_state.py
import os
import math
import pwd
import pytest

def test_final_output_exists_and_correct():
    log_path = "/home/user/project/final_output.log"
    assert os.path.isfile(log_path), f"Output file {log_path} does not exist. Did you run ./sim_app and redirect output?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content, "final_output.log is empty."

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"final_output.log contains non-numeric data: {content}")

    assert not math.isnan(val), "The computed value is NaN. Numerical instability was not fixed properly."
    assert 0.99 < val < 1.01, f"The computed value {val} is not close to 1.0. Numerical instability was not fixed or incorrect input was used."

def test_config_file_exists():
    try:
        uid = pwd.getpwnam("user").pw_uid
    except KeyError:
        uid = 1000

    config_path = f"/tmp/.sim_config_{uid}.dat"
    assert os.path.isfile(config_path), f"Configuration file {config_path} is missing. Did you use strace to find the required file path?"

    with open(config_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
        assert val > 0 and val < 1e-10, f"Config file contains {val}, expected a small value like 1e-15."
    except ValueError:
        pytest.fail(f"Config file contains non-numeric data: {content}")

def test_env_sh_fixed():
    env_path = "/home/user/project/env.sh"
    assert os.path.isfile(env_path), f"Environment script {env_path} is missing."
    with open(env_path, "r") as f:
        content = f.read()
    assert "-L/invalid/path/that/breaks/build" not in content, "env.sh still contains the invalid LDFLAGS path."