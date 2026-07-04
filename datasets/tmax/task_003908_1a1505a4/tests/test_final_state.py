# test_final_state.py

import os
import pytest

def compute_expected_total_steps():
    def sim(start):
        x = start
        steps = 0
        while x < 100:
            diff = 100 - x
            step = diff // 2
            if step == 0:
                step = 1
            x += step
            steps += 1
        return steps

    return sum(sim(start) for start in range(-100, 51))

def test_result_file_exists_and_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"{result_path} does not exist. Did you redirect the output?"

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected_steps = str(compute_expected_total_steps())

    # Check if the expected steps is in the output (handling potential extra whitespace/newlines)
    assert expected_steps in content.split(), f"Expected {expected_steps} in {result_path}, but got '{content}'"

def test_main_rs_exists():
    main_rs_path = "/home/user/stat_sim/src/main.rs"
    assert os.path.isfile(main_rs_path), f"{main_rs_path} does not exist. Did you delete the source file?"