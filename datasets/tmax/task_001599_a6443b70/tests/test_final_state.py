# test_final_state.py

import os
import re

def test_etl_processor_c_exists():
    path = "/home/user/etl_processor.c"
    assert os.path.isfile(path), f"Source file {path} does not exist."

def test_etl_processor_executable():
    path = "/home/user/etl_processor"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile the C program?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_pipeline_test_sh_executable():
    path = "/home/user/pipeline_test.sh"
    assert os.path.isfile(path), f"Bash script {path} does not exist."
    # The instructions don't strictly require the bash script to be executable, but it's a script.
    # We will just check if it exists and has content.
    with open(path, "r") as f:
        content = f.read().strip()
    assert len(content) > 0, f"Script {path} is empty."

def test_test_result_txt():
    path = "/home/user/test_result.txt"
    assert os.path.isfile(path), f"Result file {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "REPRODUCIBLE: YES", f"Expected 'REPRODUCIBLE: YES' in {path}, got '{content}'."

def test_csv_outputs_format():
    files_to_check = [
        "/home/user/etl_output.csv",
        "/home/user/run1.csv",
        "/home/user/run2.csv"
    ]

    # Regex for exactly: 42,posterior_mean,bootstrap_se (floats to 6 decimal places)
    pattern = re.compile(r"^42,-?\d+\.\d{6},\d+\.\d{6}$")

    for path in files_to_check:
        assert os.path.isfile(path), f"Output file {path} does not exist."
        with open(path, "r") as f:
            content = f.read().strip()

        # The file might have multiple lines if the student didn't clear it, but the instruction says "Writes the results... in the exact format".
        lines = content.splitlines()
        assert len(lines) == 1, f"Expected exactly 1 line in {path}, found {len(lines)}."

        match = pattern.match(lines[0])
        assert match, f"Content of {path} ('{lines[0]}') does not match the required format 'seed,posterior_mean,bootstrap_se' with 6 decimal places."