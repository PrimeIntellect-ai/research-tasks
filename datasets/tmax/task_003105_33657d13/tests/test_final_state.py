# test_final_state.py

import os
import math
import pytest

def test_pipeline_c_fixed():
    pipeline_path = "/home/user/pipeline.c"
    assert os.path.isfile(pipeline_path), f"File {pipeline_path} does not exist."

    with open(pipeline_path, "r") as f:
        content = f.read()

    # Check that the abort logic on WAL corruption is removed or bypassed
    # A common fix is to replace exit(1) with continue
    assert "exit(1)" not in content[content.find("sscanf") : content.find("if (id >=")] or "continue" in content, \
        "pipeline.c still aborts on WAL corruption instead of ignoring the line."

    # Check that the convergence loop uses absolute difference
    assert "fabs(" in content or "abs(" in content or "(old_val - values[0] < 0" in content or "diff = values[0] - old_val" in content, \
        "pipeline.c does not seem to calculate the absolute difference in the convergence loop."

def test_pipeline_executable_exists():
    exe_path = "/home/user/pipeline"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_output_txt_correct():
    out_path = "/home/user/output.txt"
    assert os.path.isfile(out_path), f"Output file {out_path} does not exist. Did you run the pipeline?"

    # Compute expected values identically to the fixed C logic
    values = [20.0, 10.0, -5.5]
    diff = 100.0
    iterations = 0

    while diff > 0.001 and iterations < 1000:
        old_val = values[0]
        values[0] = (values[0] + values[1] + values[2]) / 3.0
        diff = abs(old_val - values[0])
        iterations += 1

    expected_state = f"Final State: {values[0]:.3f} {values[1]:.3f} {values[2]:.3f}"
    expected_iters = f"Iterations: {iterations}"

    with open(out_path, "r") as f:
        content = f.read()

    assert expected_state in content, f"output.txt does not contain the correct final state. Expected: '{expected_state}'"
    assert expected_iters in content, f"output.txt does not contain the correct iterations count. Expected: '{expected_iters}'"