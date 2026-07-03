# test_final_state.py

import os
import pytest

def test_mre_c_exists_and_correct():
    path = "/home/user/app/mre.c"
    assert os.path.isfile(path), f"MRE file {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    assert "<calc_utils.h>" in content, f"{path} is missing <calc_utils.h> include."
    assert "<stdio.h>" in content, f"{path} is missing <stdio.h> include."
    assert "main" in content, f"{path} is missing main function."
    assert "10.0" in content, f"{path} does not initialize x to 10.0."
    assert "10" in content, f"{path} does not seem to have a 10-iteration loop."
    assert "UPDATE_RATE" in content, f"{path} does not use UPDATE_RATE."
    assert "%.2f" in content, f"{path} does not print to 2 decimal places."

def test_build_sh_fixed():
    path = "/home/user/app/build.sh"
    assert os.path.isfile(path), f"Build script {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    idx_v2 = content.find("-I/home/user/app/deps/v2")
    idx_v1 = content.find("-I/home/user/app/deps/v1")

    assert idx_v2 != -1, f"{path} must include deps/v2."

    if idx_v1 != -1:
        assert idx_v2 < idx_v1, f"In {path}, deps/v2 must be prioritized over deps/v1."

def test_solution_txt_correct():
    path = "/home/user/app/solution.txt"
    assert os.path.isfile(path), f"Solution file {path} is missing."
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"{path} must contain at least two lines."
    assert lines[0] == "Converged value: 0.000000", f"First line of {path} is incorrect. Expected 'Converged value: 0.000000'."
    assert lines[1] == "v1", f"Second line of {path} is incorrect. Expected 'v1'."