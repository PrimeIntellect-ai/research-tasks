# test_final_state.py

import os
import subprocess
import pytest
import math

def test_api_key_recovered():
    key_file = "/home/user/api_key.txt"
    assert os.path.isfile(key_file), f"File {key_file} does not exist."
    with open(key_file, "r") as f:
        content = f.read().strip()
    assert content == "sk_live_9f8e7d6c5b4a3f2e1d0c", f"Incorrect API key recovered. Found: {content}"

def test_calc_c_fixed_math():
    calc_file = "/home/user/calc_service/calc.c"
    assert os.path.isfile(calc_file), f"File {calc_file} does not exist."
    with open(calc_file, "r") as f:
        content = f.read()

    # Check that the unstable subtraction is gone or replaced by the stable addition
    # The stable form usually involves dividing by (sqrt(...) + x)
    assert "+" in content and "sqrt" in content, "The C file does not seem to contain the stable mathematical formula."
    assert "sqrt(x * x + 1.0) - x" not in content.replace(" ", ""), "The unstable formula is still present in the code."

def test_calc_compiles_and_runs():
    calc_file = "/home/user/calc_service/calc.c"
    out_file = "/home/user/calc_service/calc"

    # Compile
    compile_res = subprocess.run(
        ["gcc", "-lm", calc_file, "-o", out_file],
        capture_output=True,
        text=True
    )
    assert compile_res.returncode == 0, f"Compilation failed:\n{compile_res.stderr}"

    # Run with large input
    run_res = subprocess.run(
        [out_file, "100000000"],
        capture_output=True,
        text=True,
        timeout=2.0
    )
    assert run_res.returncode == 0, f"Execution failed with code {run_res.returncode}:\n{run_res.stderr}"

    output = run_res.stdout.strip()
    assert output, "No output from calc program."
    assert "nan" not in output.lower(), "Output is NaN."
    assert "inf" not in output.lower(), "Output is Inf."

    try:
        val = float(output)
        assert math.isfinite(val), "Output value is not finite."
    except ValueError:
        pytest.fail(f"Output '{output}' is not a valid float.")

def test_test_script():
    script_file = "/home/user/calc_service/test.sh"
    assert os.path.isfile(script_file), f"Script {script_file} does not exist."
    assert os.access(script_file, os.X_OK), f"Script {script_file} is not executable."

    with open(script_file, "r") as f:
        content = f.read()
    assert "timeout" in content, "The test script does not use the 'timeout' command."

    run_res = subprocess.run(
        ["bash", script_file],
        cwd="/home/user/calc_service",
        capture_output=True,
        text=True
    )
    assert run_res.returncode == 0, f"Test script failed with code {run_res.returncode}:\n{run_res.stderr}\n{run_res.stdout}"