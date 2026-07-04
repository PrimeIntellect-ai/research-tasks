# test_final_state.py

import os
import pytest

def test_result_file_exists():
    assert os.path.isfile("/home/user/result.txt"), "result.txt does not exist at /home/user/result.txt"

def test_result_value_converged():
    try:
        with open("/home/user/result.txt", "r") as f:
            val_str = f.read().strip()
            val = float(val_str)
    except ValueError:
        pytest.fail(f"result.txt does not contain a valid floating-point number. Found: '{val_str}'")
    except Exception as e:
        pytest.fail(f"Could not read result.txt: {e}")

    assert 10.8 <= val <= 11.2, f"Value {val} in result.txt is outside the expected convergence range (10.8 - 11.2)."

def test_makefile_fixed():
    makefile_path = "/home/user/consensus_debugger/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-lm" in content, "Makefile does not contain the '-lm' linker flag required to fix the compilation error."

def test_executable_exists():
    exe_path = "/home/user/consensus_debugger/sim"
    assert os.path.isfile(exe_path), "The compiled 'sim' executable does not exist. Did you run make?"
    assert os.access(exe_path, os.X_OK), "The 'sim' file is not executable."

def test_sim_c_fixed():
    sim_c_path = "/home/user/consensus_debugger/sim.c"
    assert os.path.isfile(sim_c_path), "sim.c is missing."
    with open(sim_c_path, "r") as f:
        content = f.read()
    assert "double alpha = 1.2;" not in content, "sim.c still contains the buggy 'double alpha = 1.2;' line."