# test_final_state.py

import os
import subprocess
import pytest

def test_mre_csv_content():
    path = "/home/user/mre.csv"
    assert os.path.isfile(path), f"MRE file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "-17,Malicious_User,999"
    assert content == expected, f"Expected {path} to contain exactly '{expected}', but got '{content}'."

def test_ticket_resolution_content():
    path = "/home/user/ticket_resolution.txt"
    assert os.path.isfile(path), f"Resolution report {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {path}, but found {len(lines)}."
    assert lines[0] == "-17", f"Expected line 1 to be '-17', but got '{lines[0]}'."
    assert lines[1] == "734", f"Expected line 2 to be '734', but got '{lines[1]}'."

def test_csv_transformer_fixed_and_compiles():
    source_path = "/home/user/csv_transformer.c"
    binary_path = "/home/user/csv_transformer_test_bin"
    data_path = "/home/user/data/customer_records.csv"

    assert os.path.isfile(source_path), f"Source file {source_path} does not exist."
    assert os.path.isfile(data_path), f"Data file {data_path} does not exist."

    # Recompile the source code to ensure the fix is actually in the C file
    compile_proc = subprocess.run(
        ["gcc", "-g", "-o", binary_path, source_path],
        capture_output=True,
        text=True
    )
    assert compile_proc.returncode == 0, f"Compilation of {source_path} failed:\n{compile_proc.stderr}"

    # Run the compiled binary against the data file
    run_proc = subprocess.run(
        [binary_path, data_path],
        capture_output=True,
        text=True
    )

    # Clean up the test binary
    if os.path.exists(binary_path):
        os.remove(binary_path)

    assert run_proc.returncode == 0, (
        f"Running the patched program failed with exit code {run_proc.returncode}.\n"
        f"Stderr: {run_proc.stderr}\n"
        f"Stdout: {run_proc.stdout}"
    )