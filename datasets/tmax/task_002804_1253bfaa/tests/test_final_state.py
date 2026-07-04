# test_final_state.py

import os
import re

def test_runner_c_exists():
    assert os.path.isfile("/home/user/runner.c"), "The file /home/user/runner.c does not exist."

def test_makefile_exists_and_content():
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), f"The file {makefile_path} does not exist."

    with open(makefile_path, 'r') as f:
        content = f.read()

    assert "-Wall" in content, "Makefile is missing the '-Wall' flag."
    assert "-Wextra" in content, "Makefile is missing the '-Wextra' flag."
    assert "-O2" in content, "Makefile is missing the '-O2' flag."
    assert re.search(r"^clean:", content, re.MULTILINE), "Makefile is missing the 'clean' target."

def test_execution_log_content():
    log_path = "/home/user/execution.log"
    assert os.path.isfile(log_path), f"The file {log_path} does not exist. Did you run the compiled tool?"

    expected_lines = [
        "Step 1: Linux setup complete",
        "Step 2: Memory check passed",
        "Step 4: Memory limit check passed"
    ]

    with open(log_path, 'r') as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"The contents of {log_path} do not match the expected output. Got:\n{content}"