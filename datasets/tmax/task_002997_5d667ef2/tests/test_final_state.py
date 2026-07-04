# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
SOLUTION_FILE = "/home/user/solution.txt"
CONFIG_KEY_FILE = os.path.join(PROJECT_DIR, "config.key")

def test_solution_file_exists_and_correct():
    assert os.path.isfile(SOLUTION_FILE), f"Solution file {SOLUTION_FILE} is missing."

    with open(SOLUTION_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"{SOLUTION_FILE} must contain at least two lines."
    assert lines[0] == "AUTH_8f9c2b_TEST", f"First line of {SOLUTION_FILE} is incorrect. Expected 'AUTH_8f9c2b_TEST', got '{lines[0]}'."
    assert lines[1] == "loop_counter", f"Second line of {SOLUTION_FILE} is incorrect. Expected 'loop_counter', got '{lines[1]}'."

def test_config_key_restored():
    assert os.path.isfile(CONFIG_KEY_FILE), f"File {CONFIG_KEY_FILE} was not restored."
    with open(CONFIG_KEY_FILE, "r") as f:
        content = f.read().strip()
    assert content == "AUTH_8f9c2b_TEST", f"Content of {CONFIG_KEY_FILE} is incorrect."

def test_c_code_compiles_and_tests_pass_reliably():
    # Compile the code
    make_process = subprocess.run(
        ["make"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert make_process.returncode == 0, f"Compilation failed:\n{make_process.stderr}"

    # Run the tests 50 times to ensure intermittent bug is fixed
    run_tests_script = os.path.join(PROJECT_DIR, "run_tests.sh")
    assert os.path.isfile(run_tests_script), f"{run_tests_script} is missing."

    for i in range(50):
        test_process = subprocess.run(
            [run_tests_script],
            cwd=PROJECT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert test_process.returncode == 0, (
            f"Test execution failed on run {i+1}.\n"
            f"STDOUT: {test_process.stdout}\n"
            f"STDERR: {test_process.stderr}\n"
            "This indicates the uninitialized variable bug might not be fully fixed."
        )