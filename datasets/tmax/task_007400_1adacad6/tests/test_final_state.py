# test_final_state.py
import os
import json
import stat
import pytest

QA_ENV_DIR = "/home/user/qa_env"

def get_expected_dot_product():
    vectors_file = os.path.join(QA_ENV_DIR, "vectors.json")
    assert os.path.isfile(vectors_file), f"File {vectors_file} is missing."
    with open(vectors_file, 'r') as f:
        data = json.load(f)
    x = data.get("vector_x", [])
    y = data.get("vector_y", [])
    assert len(x) == len(y), "vector_x and vector_y must have the same length."
    return sum(a * b for a, b in zip(x, y))

def test_config_h():
    expected_dp = get_expected_dot_product()
    config_h = os.path.join(QA_ENV_DIR, "config.h")
    assert os.path.isfile(config_h), f"File {config_h} is missing."

    with open(config_h, 'r') as f:
        content = f.read().strip()

    expected_line = f"#define DOT_PRODUCT {expected_dp}"
    assert expected_line in content, f"config.h does not contain the expected macro definition. Expected to find: {expected_line}"

def test_makefile_patched():
    makefile = os.path.join(QA_ENV_DIR, "Makefile")
    assert os.path.isfile(makefile), f"File {makefile} is missing."

    with open(makefile, 'r') as f:
        content = f.read()

    assert "-I/nonexistent/path" not in content, "Makefile still contains the broken include path '-I/nonexistent/path'."
    assert "-I." in content, "Makefile does not contain the fixed include path '-I.'."
    assert "main.o: main.c config.h" in content, "Makefile does not contain the fixed dependencies for main.o."

def test_math_eval_compiled():
    math_eval = os.path.join(QA_ENV_DIR, "math_eval")
    assert os.path.isfile(math_eval), f"Compiled binary {math_eval} is missing."

    st = os.stat(math_eval)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"File {math_eval} is not executable."

def test_result_txt():
    expected_dp = get_expected_dot_product()
    result_txt = os.path.join(QA_ENV_DIR, "result.txt")
    assert os.path.isfile(result_txt), f"File {result_txt} is missing."

    with open(result_txt, 'r') as f:
        content = f.read().strip()

    expected_content = f"Test Output Verification: {expected_dp}"
    assert content == expected_content, f"result.txt content is incorrect.\nExpected: '{expected_content}'\nGot: '{content}'"