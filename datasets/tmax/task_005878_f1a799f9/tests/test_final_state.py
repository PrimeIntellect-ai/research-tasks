# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_hash():
    student_file = "/home/user/bad_commit.txt"
    expected_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(student_file), f"Deliverable {student_file} does not exist."
    assert os.path.isfile(expected_file), f"Truth file {expected_file} is missing."

    with open(student_file, "r") as f:
        student_hash = f.read().strip()

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    assert student_hash == expected_hash, f"Incorrect bad commit hash. Expected {expected_hash}, got {student_hash}."

def test_fixed_processor_compiles_and_runs():
    fixed_src = "/home/user/fixed_processor.cpp"
    assert os.path.isfile(fixed_src), f"Deliverable {fixed_src} does not exist."

    executable = "/tmp/proc_test"

    # Compile the fixed source code
    compile_cmd = ["g++", "-O3", "-pthread", fixed_src, "-o", executable]
    try:
        subprocess.run(compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Compilation failed:\n{e.stderr}")

    assert os.path.isfile(executable), "Executable was not created after compilation."

    # Run the executable 5 times to ensure no race condition
    for i in range(5):
        try:
            result = subprocess.run([executable], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout.strip()
            assert output == "10000000", f"Run {i+1} failed: Expected output '10000000', got '{output}'."
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Execution {i+1} failed:\n{e.stderr}")