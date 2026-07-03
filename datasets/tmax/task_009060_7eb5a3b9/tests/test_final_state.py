# test_final_state.py

import os
import subprocess
import pytest

def test_binary_exists_and_executable():
    bin_path = "/home/user/bin/score_seq"
    assert os.path.exists(bin_path), f"Executable {bin_path} does not exist."
    assert os.path.isfile(bin_path), f"Path {bin_path} is not a file."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_script_fixed():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    with open(script_path, "r") as f:
        content = f.read()

    assert "sort" in content, f"Script {script_path} does not contain 'sort' command."
    assert "/home/user/bin/score_seq" in content, f"Script {script_path} does not call the expected binary path."

def test_reproducible_output():
    out_path = "/home/user/reproducible_output.txt"
    assert os.path.exists(out_path), f"Output file {out_path} does not exist."
    assert os.path.isfile(out_path), f"Path {out_path} is not a file."

    # Compute expected output
    c_source = "/home/user/src/score_seq.c"
    tmp_bin = "/tmp/test_score_seq"

    # Compile the truth binary to get the exact expected floating point reduction
    try:
        subprocess.run(["gcc", c_source, "-o", tmp_bin], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile the C source code for verification. Error: {e.stderr.decode()}")

    # Get sorted file paths
    seq_dir = "/home/user/seq_data"
    files = sorted([os.path.join(seq_dir, f) for f in os.listdir(seq_dir) if f.endswith(".dat")])
    input_data = "\n".join(files) + "\n"

    # Run the compiled truth binary
    try:
        result = subprocess.run([tmp_bin], input=input_data.encode(), stdout=subprocess.PIPE, check=True)
        expected_output = result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run the verification binary. Error: {e.stderr.decode()}")

    # Read actual output
    with open(out_path, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Output in {out_path} does not match expected reproducible output.\n"
        f"Expected: {expected_output}\n"
        f"Actual: {actual_output}"
    )