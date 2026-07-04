# test_final_state.py

import os
import re
import pytest

def test_result_file():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert "FINAL: 2000.0002" in content, f"Expected 'FINAL: 2000.0002' in {result_path}, but found: {content}"

def test_simulator_cpp_fixed():
    cpp_path = "/home/user/sim_project/simulator.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} is missing."

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "float current_pos" not in content, "current_pos is still declared as float."
    assert "float v, dt" not in content and "float v" not in content and "float dt" not in content, "v or dt are still declared as float."

    assert re.search(r"double\s+current_pos", content), "current_pos must be declared as double."
    assert re.search(r"double\s+v\s*,\s*dt|double\s+v\s*;\s*double\s+dt|double\s+dt\s*,\s*v", content), "v and dt must be declared as double."

def test_simulator_compiled():
    binary_path = "/home/user/sim_project/simulator"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."