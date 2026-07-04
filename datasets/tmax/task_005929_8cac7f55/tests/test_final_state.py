# test_final_state.py

import os
import stat
import subprocess
import pytest
import re

PROJECT_DIR = "/home/user/polyglot-eval"
BUILD_AND_RUN_SCRIPT = os.path.join(PROJECT_DIR, "build_and_run.sh")
CMAKELISTS = os.path.join(PROJECT_DIR, "CMakeLists.txt")
TEST_RUNNER = os.path.join(PROJECT_DIR, "tests/test_runner.cpp")
RESULTS_TXT = os.path.join(PROJECT_DIR, "results.txt")
GENERATE_DATA = os.path.join(PROJECT_DIR, "scripts/generate_data.py")
EXPR_EVAL_BIN = os.path.join(PROJECT_DIR, "build/expr_eval")

def test_build_and_run_script_exists_and_executable():
    assert os.path.isfile(BUILD_AND_RUN_SCRIPT), f"{BUILD_AND_RUN_SCRIPT} does not exist."
    st = os.stat(BUILD_AND_RUN_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{BUILD_AND_RUN_SCRIPT} is not executable."

def test_cmake_lists_exists_and_targets():
    assert os.path.isfile(CMAKELISTS), f"{CMAKELISTS} does not exist."
    with open(CMAKELISTS, "r") as f:
        content = f.read()

    assert "expr_lib" in content, "CMakeLists.txt does not contain 'expr_lib' target."
    assert "expr_eval" in content, "CMakeLists.txt does not contain 'expr_eval' target."
    assert "test_runner" in content, "CMakeLists.txt does not contain 'test_runner' target."

def test_test_runner_exists():
    assert os.path.isfile(TEST_RUNNER), f"{TEST_RUNNER} does not exist."
    with open(TEST_RUNNER, "r") as f:
        content = f.read()
    assert "ast.h" in content, "test_runner.cpp does not include ast.h"
    assert "evaluator.h" in content, "test_runner.cpp does not include evaluator.h"

def test_build_and_run_execution():
    # Run the build_and_run.sh script
    result = subprocess.run(
        [BUILD_AND_RUN_SCRIPT],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"build_and_run.sh failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_results_txt_content():
    assert os.path.isfile(RESULTS_TXT), f"{RESULTS_TXT} was not created."

    # Dynamically compute expected results by running the python script
    gen_result = subprocess.run(
        ["python3", GENERATE_DATA],
        stdout=subprocess.PIPE,
        text=True,
        check=True
    )

    expected_results = []
    for line in gen_result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        try:
            # Safely evaluate the simple math expressions
            val = eval(line)
            expected_results.append(str(val))
        except Exception:
            pass

    with open(RESULTS_TXT, "r") as f:
        actual_results = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_results) == len(expected_results), f"Expected {len(expected_results)} results, got {len(actual_results)} in results.txt"

    for i, (actual, expected) in enumerate(zip(actual_results, expected_results)):
        assert actual == expected, f"Mismatch at line {i+1}: expected {expected}, got {actual}"

def test_valgrind_clean():
    assert os.path.isfile(EXPR_EVAL_BIN), f"Executable {EXPR_EVAL_BIN} not found. Did the build succeed?"

    # Run valgrind on the built executable
    gen_result = subprocess.run(
        ["python3", GENERATE_DATA],
        stdout=subprocess.PIPE,
        check=True
    )

    valgrind_cmd = [
        "valgrind",
        "--leak-check=full",
        "--error-exitcode=1",
        EXPR_EVAL_BIN
    ]

    result = subprocess.run(
        valgrind_cmd,
        input=gen_result.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"Valgrind reported memory errors or leaks.\nSTDERR:\n{result.stderr}"