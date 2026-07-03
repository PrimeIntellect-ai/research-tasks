# test_final_state.py

import os
import json
import subprocess
import pytest

def test_files_exist():
    """Verify that all required files have been created."""
    assert os.path.isfile("/home/user/simulate.c"), "Missing /home/user/simulate.c"
    assert os.path.isfile("/home/user/workflow.ipynb"), "Missing /home/user/workflow.ipynb"
    assert os.path.isfile("/home/user/best_fit.json"), "Missing /home/user/best_fit.json"

def test_best_fit_json_content():
    """Verify the contents of the best_fit.json file."""
    json_path = "/home/user/best_fit.json"
    assert os.path.isfile(json_path), f"Missing {json_path}"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON")

    assert "best_r" in data, "Missing 'best_r' in best_fit.json"
    assert "best_K" in data, "Missing 'best_K' in best_fit.json"
    assert "min_sse" in data, "Missing 'min_sse' in best_fit.json"

    assert abs(data["best_r"] - 0.2) < 1e-5, f"Expected best_r to be 0.2, got {data['best_r']}"
    assert abs(data["best_K"] - 400.0) < 1e-5, f"Expected best_K to be 400.0, got {data['best_K']}"
    assert isinstance(data["min_sse"], float) or isinstance(data["min_sse"], int), "min_sse must be a number"

def test_c_program_compiles_and_runs():
    """Verify that simulate.c compiles and runs correctly."""
    c_file = "/home/user/simulate.c"
    exe_file = "/home/user/verify_sim"
    csv_file = "/home/user/population_data.csv"

    assert os.path.isfile(c_file), f"Missing {c_file}"

    # Compile the C program
    compile_cmd = ["gcc", "-o", exe_file, c_file, "-lm"]
    compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_result.returncode == 0, f"Compilation failed:\n{compile_result.stderr}"

    assert os.path.isfile(exe_file), "Executable was not created after compilation"

    # Run the C program
    run_cmd = [exe_file, csv_file, "0.2", "400.0"]
    run_result = subprocess.run(run_cmd, capture_output=True, text=True)
    assert run_result.returncode == 0, f"Execution failed:\n{run_result.stderr}"

    # Check output is a float
    output = run_result.stdout.strip()
    try:
        sse = float(output)
    except ValueError:
        pytest.fail(f"C program output is not a valid float: {output}")

    assert sse >= 0, "SSE should be non-negative"