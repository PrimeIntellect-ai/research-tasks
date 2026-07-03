# test_final_state.py
import os
import json
import subprocess
import pytest

def test_c_code_fixed():
    c_path = "/home/user/score_fasta.c"
    assert os.path.isfile(c_path), f"File not found: {c_path}"

    with open(c_path, 'r') as f:
        content = f.read()

    assert "#pragma omp atomic" not in content, "The C code still uses '#pragma omp atomic'"

def test_c_code_compiles_and_runs():
    c_path = "/home/user/score_fasta.c"
    exe_path = "/home/user/score_fasta"

    # Compile
    compile_cmd = ["gcc", "-O3", "-fopenmp", c_path, "-o", exe_path]
    res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Compilation failed: {res.stderr}"

    # Run
    run_cmd = [exe_path, "/home/user/input.fasta"]
    res = subprocess.run(run_cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Execution failed: {res.stderr}"

    # Output should be a float
    try:
        val = float(res.stdout.strip())
    except ValueError:
        pytest.fail(f"Output is not a valid float: {res.stdout}")

def test_final_report_exists_and_valid():
    report_path = "/home/user/final_report.json"
    assert os.path.isfile(report_path), f"File not found: {report_path}"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("final_report.json is not valid JSON")

    assert "deterministic" in data, "Missing 'deterministic' key"
    assert data["deterministic"] is True, "'deterministic' should be true"

    assert "p_value" in data, "Missing 'p_value' key"
    assert isinstance(data["p_value"], float), "'p_value' should be a float"

    assert "mean_score" in data, "Missing 'mean_score' key"
    assert isinstance(data["mean_score"], float), "'mean_score' should be a float"