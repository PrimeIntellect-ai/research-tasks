# test_final_state.py

import os
import subprocess
import math

def test_feature_trace_output():
    trace_file = "/home/user/feature_trace.txt"
    assert os.path.isfile(trace_file), f"Output file {trace_file} is missing"

    with open(trace_file, "r") as f:
        content = f.read().strip()

    try:
        trace_val = float(content)
    except ValueError:
        assert False, f"Content of {trace_file} is not a valid float: '{content}'"

    # Expected trace value with jitter 1e-5
    # cov = [[0.5, 0, 0], [0, 0.5, 0], [0, 0, 0]]
    # jittered = [[0.50001, 0, 0], [0, 0.50001, 0], [0, 0, 0.00001]]
    # L diagonal = [sqrt(0.50001), sqrt(0.50001), sqrt(0.00001)]
    expected_trace = math.sqrt(0.50001) + math.sqrt(0.50001) + math.sqrt(0.00001)

    assert math.isclose(trace_val, expected_trace, rel_tol=1e-4, abs_tol=1e-4), \
        f"Trace value {trace_val} is not within tolerance of expected {expected_trace}"

def test_rust_test_exists_and_passes():
    main_rs = "/home/user/pdb_feature_extractor/src/main.rs"
    assert os.path.isfile(main_rs), f"File {main_rs} is missing"

    with open(main_rs, "r") as f:
        content = f.read()

    assert "test_planar_jitter" in content, "The test 'test_planar_jitter' was not found in src/main.rs"

    # Run cargo test
    result = subprocess.run(
        ["cargo", "test"],
        cwd="/home/user/pdb_feature_extractor",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"'cargo test' failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert "test_planar_jitter" in result.stdout or "test_planar_jitter" in result.stderr, \
        "The test 'test_planar_jitter' does not appear to have been run by cargo test"