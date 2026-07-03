# test_final_state.py

import os
import subprocess
import pytest

def test_minimal_repro_txt():
    path = "/home/user/minimal_repro.txt"
    assert os.path.isfile(path), f"Missing {path}"
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == "-14", f"Expected minimal_repro.txt to contain '-14', but got '{content}'"

def test_math_worker_fixed_cpp():
    path = "/home/user/math_worker_fixed.cpp"
    assert os.path.isfile(path), f"Missing {path}"
    with open(path, 'r') as f:
        content = f.read()
    assert "mutex" in content, "Expected to find 'mutex' in math_worker_fixed.cpp to prevent interleaving"

def test_math_worker_fixed_executable():
    path = "/home/user/math_worker_fixed"
    assert os.path.isfile(path), f"Missing compiled executable at {path}"
    assert os.access(path, os.X_OK), f"File {path} is not executable"

def test_parser_fixed_execution():
    parser_path = "/home/user/parser_fixed.py"
    data_path = "/home/user/data_batch.txt"
    assert os.path.isfile(parser_path), f"Missing {parser_path}"

    try:
        # Run the fixed parser on the data batch; it should exit with code 0
        subprocess.check_call(
            ["python3", parser_path, data_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"parser_fixed.py failed to process data_batch.txt. Exit code: {e.returncode}")
    except subprocess.TimeoutExpired:
        pytest.fail("parser_fixed.py timed out while processing data_batch.txt")

def test_interleaved_trace_log():
    path = "/home/user/interleaved_trace.log"
    assert os.path.isfile(path), f"Missing {path}"
    with open(path, 'r') as f:
        content = f.read().strip()
    assert len(content) > 0, f"Expected {path} to contain a snippet of the interleaved output, but it is empty"