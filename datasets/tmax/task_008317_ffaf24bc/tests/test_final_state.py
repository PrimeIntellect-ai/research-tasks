# test_final_state.py

import os

def test_answer_file_exists_and_correct():
    answer_path = "/home/user/answer.txt"
    assert os.path.isfile(answer_path), f"Expected answer file at {answer_path} is missing."

    with open(answer_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines in {answer_path}, found {len(lines)}."

    secret_key = lines[0]
    log_id = lines[1]

    assert secret_key == "MATH_SEC_88291", f"The recovered secret key on line 1 is incorrect. Got: {secret_key}"
    assert log_id == "LOG_409", f"The Log ID on line 2 is incorrect. Got: {log_id}"

def test_libmathops_compiled():
    so_path = "/home/user/pipeline_repo/libmathops.so"
    assert os.path.isfile(so_path), f"The shared library {so_path} was not compiled. Did you fix the Makefile and build it?"