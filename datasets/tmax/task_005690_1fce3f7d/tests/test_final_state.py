# test_final_state.py
import os
import subprocess
import pytest

def test_failing_input_txt():
    file_path = "/home/user/ticket_882/failing_input.txt"
    assert os.path.exists(file_path), f"File {file_path} does not exist."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "256", f"Expected failing_input.txt to contain '256', but found '{content}'."

def test_factorize_c_fixed():
    file_path = "/home/user/ticket_882/factorize.c"
    assert os.path.exists(file_path), f"Source code file {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read()

    # Check that the buggy buffer and assertion are gone or modified to >= 32
    # The hint says safely size the buffers/assertions to 32.
    # We won't strictly parse C, but we can verify it compiles and runs correctly.
    # However, we can check that "factors[8]" and "assert(count < 8)" are not present.
    assert "factors[8]" not in content.replace(" ", ""), "The source code still contains the buggy buffer size 8."
    assert "assert(count<8)" not in content.replace(" ", ""), "The source code still contains the buggy assertion for size 8."

def test_factorize_executable():
    exe_path = "/home/user/ticket_882/factorize"
    assert os.path.exists(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

    # Run the executable with 256, which previously failed
    try:
        result = subprocess.run([exe_path, "256"], capture_output=True, text=True, timeout=2)
    except subprocess.TimeoutExpired:
        pytest.fail("The factorize program timed out when running with input 256.")

    assert result.returncode == 0, f"The factorize program failed with input 256. Stderr: {result.stderr}"
    assert "256: 2 2 2 2 2 2 2 2" in result.stdout, "The factorize program did not output the correct factors for 256."

    # Run with a number that has more than 8 factors to ensure the fix actually works
    # e.g., 512 has 9 factors
    try:
        result_512 = subprocess.run([exe_path, "512"], capture_output=True, text=True, timeout=2)
    except subprocess.TimeoutExpired:
        pytest.fail("The factorize program timed out when running with input 512.")

    assert result_512.returncode == 0, f"The factorize program failed with input 512. Stderr: {result_512.stderr}"
    assert "512: 2 2 2 2 2 2 2 2 2" in result_512.stdout, "The factorize program did not output the correct factors for 512."