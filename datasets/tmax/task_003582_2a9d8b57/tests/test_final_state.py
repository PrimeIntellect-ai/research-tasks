# test_final_state.py

import os
import subprocess
import pytest

def test_eval_service_orig_exists():
    path = "/home/user/eval_service_orig"
    assert os.path.isfile(path), f"Original compiled service {path} is missing."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_leak_bytes_correct():
    path = "/home/user/leak_bytes.txt"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "48", f"Expected 48 leaked bytes, but got '{content}' in {path}."

def test_fixed_eval_c_exists():
    path = "/home/user/fixed_eval.c"
    assert os.path.isfile(path), f"Fixed source file {path} is missing."

def test_eval_service_exists_and_fixed():
    executable = "/home/user/eval_service"
    input_file = "/home/user/fuzz_inputs.txt"

    assert os.path.isfile(executable), f"Fixed compiled service {executable} is missing."
    assert os.access(executable, os.X_OK), f"{executable} is not executable."
    assert os.path.isfile(input_file), f"Input file {input_file} is missing."

    # Run the fixed service with valgrind
    cmd = ["valgrind", "--leak-check=full", executable]
    with open(input_file, "r") as f:
        result = subprocess.run(cmd, stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    assert result.returncode == 0, f"eval_service crashed or returned non-zero exit code. Stderr: {result.stderr}"

    # Check for "definitely lost: 0 bytes" in valgrind output
    # Valgrind prints to stderr
    stderr_lower = result.stderr.lower()

    assert "definitely lost: 0 bytes" in stderr_lower, (
        f"Memory leak is not fully fixed. Valgrind output did not indicate 0 bytes definitely lost.\n"
        f"Valgrind output:\n{result.stderr}"
    )