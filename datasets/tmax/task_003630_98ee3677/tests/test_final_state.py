# test_final_state.py

import os
import pytest

def test_sim_fixed_executable_exists():
    """Check if the compiled executable sim_fixed exists and is executable."""
    executable_path = "/home/user/sim_profiling/sim_fixed"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist. Did you compile the code?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_final_result_exists_and_correct():
    """Check if final_result.txt exists and contains the correct sum."""
    result_path = "/home/user/sim_profiling/final_result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist. Did you run the executable and redirect output?"

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected_output = "Total Sum: 10000.0000"
    assert content == expected_output, f"Expected output '{expected_output}', but got '{content}'. Check your precision and input handling."

def test_simulation_c_modified():
    """Check if simulation.c was modified to use double precision."""
    source_path = "/home/user/sim_profiling/simulation.c"
    assert os.path.isfile(source_path), f"Source file {source_path} is missing."

    with open(source_path, "r") as f:
        content = f.read()

    # The exact variable name might change, but 'double' should be present for the accumulation.
    assert "double " in content, "The source code does not appear to use 'double' precision. You must use double for the accumulation to avoid precision loss."