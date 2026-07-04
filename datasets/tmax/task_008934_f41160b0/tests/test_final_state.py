# test_final_state.py

import os
import pytest

def test_converged_result_file():
    result_file = '/home/user/sim/converged_result.txt'
    assert os.path.isfile(result_file), f"The file {result_file} does not exist."

    with open(result_file, 'r') as f:
        content = f.read().strip()

    assert content == "10.976077", f"Expected converged result to be '10.976077', but got '{content}'."

def test_cpp_source_fixed():
    source_file = '/home/user/sim/equilibrium_sim.cpp'
    assert os.path.isfile(source_file), f"The file {source_file} does not exist."

    with open(source_file, 'r') as f:
        content = f.read()

    assert "std::execution::par" not in content, "The source file still contains 'std::execution::par', which causes non-deterministic reduction."
    assert "std::execution::par_unseq" not in content, "The source file contains 'std::execution::par_unseq', which causes non-deterministic reduction."