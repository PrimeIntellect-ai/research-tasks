# test_final_state.py

import os
import subprocess
import pytest

def test_auth_gen_c_fixed_formula():
    """Verify that the logical error in the formula has been fixed."""
    path = "/home/user/auth_gen.c"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    assert "hours * 360)" not in content and "hours * 360 " not in content, \
        "The formula error (hours * 360) is still present in auth_gen.c"

def test_verify_tokens_success():
    """Verify that the verify_tokens.py script reports success."""
    script_path = "/home/user/verify_tokens.py"
    assert os.path.isfile(script_path), f"File {script_path} is missing."

    try:
        output = subprocess.check_output(["python3", script_path], stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"verify_tokens.py failed to run. Output:\n{e.output.decode()}")

    assert "SUCCESS" in output, f"verify_tokens.py did not report SUCCESS. Output:\n{output}"

def test_auth_gen_no_crash_on_long_input():
    """Verify that auth_gen handles long timezone strings without crashing."""
    binary_path = "/home/user/auth_gen"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."

    # Create a temporary file with a long timezone string
    test_input = "/home/user/test_crash.txt"
    with open(test_input, "w") as f:
        f.write("1625000000 UTC+02:00_MALFORMED_LONG_STRING_CAUSING_CRASH_AND_MORE_A" * 10 + "\n")

    try:
        # Run the binary against the long input
        subprocess.check_output([binary_path, test_input], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        # If it crashed (e.g., negative return code like -11 for SIGSEGV), fail
        pytest.fail(f"auth_gen crashed on long input. Return code: {e.returncode}. Output:\n{e.output.decode()}")
    finally:
        if os.path.exists(test_input):
            os.remove(test_input)

def test_final_tokens_log_contents():
    """Verify the final output matches the expected correctly computed tokens."""
    log_path = "/home/user/final_tokens.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "1700000000 UTC+09:00 -> AFAB482E",
        "1700000000 UTC-08:00 -> AFAABF3E",
        "1700000000 UTC+05:45 -> AFAB7E62"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, found {len(lines)}."

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} in {log_path} does not match expected output.\nExpected: {expected}\nFound: {lines[i]}"