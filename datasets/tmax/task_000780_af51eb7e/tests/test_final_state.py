# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_c_source_file_exists():
    path = "/home/user/max_degree.c"
    assert os.path.exists(path), f"Source file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_executable_exists_and_executable():
    path = "/home/user/max_degree"
    assert os.path.exists(path), f"Executable {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

    # Check if executable
    st = os.stat(path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"{path} is not executable."

def test_result_file_content():
    path = "/home/user/result.txt"
    assert os.path.exists(path), f"Result file {path} does not exist. Did you run your pipeline and redirect output?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "MAX_NODE=extract_transactions COUNT=5"
    assert content == expected, f"Expected '{expected}' in {path}, but got '{content}'."

def test_max_degree_executable_behavior():
    executable = "/home/user/max_degree"
    if not os.path.exists(executable):
        pytest.skip(f"Executable {executable} not found, skipping behavior test.")

    # Test input: sorted list of nodes
    test_input = "nodeA\nnodeB\nnodeB\nnodeC\nnodeC\nnodeC\nnodeD\n"
    expected_output = "MAX_NODE=nodeC COUNT=3"

    try:
        process = subprocess.run(
            [executable],
            input=test_input,
            text=True,
            capture_output=True,
            check=True,
            timeout=2
        )
        output = process.stdout.strip()
        assert output == expected_output, f"Executable produced incorrect output. Expected '{expected_output}', got '{output}'."
    except subprocess.TimeoutExpired:
        pytest.fail("Executable timed out while reading standard input.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executable failed with return code {e.returncode}. Stderr: {e.stderr}")