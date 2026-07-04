# test_final_state.py
import os
import pytest

def get_expected():
    state = 42
    total_score = 0
    for _ in range(100000):
        pos = 30
        while pos > 0 and pos < 100:
            state = (1103515245 * state + 12345) & 0x7FFFFFFF
            bit = (state // 65536) % 2
            if bit == 0:
                pos -= 1
            else:
                pos += 1
        if pos == 0:
            total_score += 10
        else:
            total_score += 50
    return f"{total_score / 100000:.4f}"

def test_c_source_exists():
    assert os.path.isfile("/home/user/mc_bvp.c"), "The C source code file /home/user/mc_bvp.c does not exist."

def test_executable_exists():
    exe_path = "/home/user/mc_bvp"
    assert os.path.isfile(exe_path), f"The executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_result_file_correct():
    result_path = "/home/user/mc_pde_result.txt"
    assert os.path.isfile(result_path), f"The result file {result_path} does not exist."

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected = get_expected()
    assert content == expected, f"Expected the result file to contain '{expected}', but got '{content}'."