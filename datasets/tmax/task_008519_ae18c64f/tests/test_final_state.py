# test_final_state.py

import os
import pytest

WORK_DIR = "/home/user/ticket_8841"

def test_wrapper_c_fixed():
    wrapper_path = os.path.join(WORK_DIR, "wrapper.c")
    assert os.path.isfile(wrapper_path), f"File {wrapper_path} does not exist."
    with open(wrapper_path, "r") as f:
        content = f.read()
    assert "calc_decay_v2" in content, "wrapper.c does not contain the correct function name 'calc_decay_v2'."
    assert "calculate_decay" not in content, "wrapper.c still contains the incorrect function name 'calculate_decay'."

def test_wrapper_so_compiled():
    wrapper_so_path = os.path.join(WORK_DIR, "wrapper.so")
    assert os.path.isfile(wrapper_so_path), f"File {wrapper_so_path} does not exist. The build script was likely not run or failed."

def test_result_txt_correct():
    result_path = os.path.join(WORK_DIR, "result.txt")
    assert os.path.isfile(result_path), f"File {result_path} does not exist. simulate.py was likely not run."
    with open(result_path, "r") as f:
        content = f.read().strip()

    # 0.500000 is the expected output
    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"result.txt content '{content}' is not a valid float.")

    assert abs(val - 0.5) < 1e-4, f"result.txt contains {val}, expected 0.500000 (numerical instability not fixed)."