# test_final_state.py

import os
import json
import subprocess
import pytest

def test_report_json_exists_and_correct():
    """Verify that report.json exists and contains the correct values."""
    report_path = "/home/user/results/report.json"
    assert os.path.exists(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not a valid JSON file.")

    assert data.get("leakage_fixed") is True, "The 'leakage_fixed' key must be set to true."

    acc = data.get("corrected_test_accuracy")
    assert acc is not None, "The 'corrected_test_accuracy' key is missing."

    try:
        acc_float = float(acc)
    except ValueError:
        pytest.fail(f"corrected_test_accuracy must be a float, got {acc}")

    assert abs(acc_float - 0.5400) < 0.001, f"Expected corrected test accuracy to be ~0.5400, but got {acc_float}"

def test_c_code_fixed_and_produces_correct_output():
    """Verify that the C code has been fixed and produces the correct accuracy."""
    c_file_path = "/home/user/workspace/knn_pipeline.c"
    assert os.path.isfile(c_file_path), f"C source file {c_file_path} is missing."

    # Compile the student's C code to verify it works and produces the expected accuracy
    test_exe = "/tmp/knn_pipeline_test"
    compile_cmd = ["gcc", "-O3", "-lm", c_file_path, "-o", test_exe]
    compile_res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_res.returncode == 0, f"Failed to compile {c_file_path}:\n{compile_res.stderr}"

    # Run the compiled executable
    run_res = subprocess.run([test_exe], capture_output=True, text=True, cwd="/home/user/workspace")
    assert run_res.returncode == 0, f"Failed to run the compiled C program:\n{run_res.stderr}"

    output = run_res.stdout
    assert "0.5400" in output, f"Expected the C program output to contain the corrected accuracy (0.5400). Output was:\n{output}"

def test_executable_exists():
    """Verify that the compiled executable exists at the required path."""
    exe_path = "/home/user/workspace/knn_pipeline_fixed"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."