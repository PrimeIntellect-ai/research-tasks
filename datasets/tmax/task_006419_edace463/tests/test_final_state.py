# test_final_state.py

import os
import sys
import subprocess
import importlib.util
import pytest

def test_incident_report_content():
    report_path = "/home/user/incident_report.txt"
    assert os.path.isfile(report_path), f"Incident report missing at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in incident report, found {len(lines)}"

    assert lines[0] == "TIMESTAMP: 2024-10-27T03:14:15Z", f"Incorrect TIMESTAMP line: {lines[0]}"
    assert lines[1] == "FIXED_VOLATILITY: 0.00", f"Incorrect FIXED_VOLATILITY line: {lines[1]}"
    assert lines[2] == "BUILD_STATUS: SUCCESS", f"Incorrect BUILD_STATUS line: {lines[2]}"

def test_predictor_volatility_fixed():
    predictor_path = "/home/user/service/predictor.py"
    assert os.path.isfile(predictor_path), f"{predictor_path} is missing."

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("predictor", predictor_path)
    predictor = importlib.util.module_from_spec(spec)
    sys.modules["predictor"] = predictor
    try:
        spec.loader.exec_module(predictor)
    except Exception as e:
        pytest.fail(f"Failed to import predictor.py: {e}")

    assert hasattr(predictor, "compute_volatility"), "compute_volatility function is missing in predictor.py"

    try:
        # This will fail with ValueError: math domain error in the original buggy code
        result = predictor.compute_volatility([1e10, 1e10, 1e10])
    except Exception as e:
        pytest.fail(f"compute_volatility threw an exception on large floats: {e}")

    assert abs(result - 0.0) < 1e-5, f"Expected volatility to be 0.0, got {result}"

def test_build_script_fixed():
    build_path = "/home/user/service/build.py"
    assert os.path.isfile(build_path), f"{build_path} is missing."

    with open(build_path, "r") as f:
        content = f.read()

    assert "<<<<<<< HEAD" not in content, "Git merge conflict markers still present in build.py"
    assert "=======" not in content, "Git merge conflict markers still present in build.py"
    assert ">>>>>>>" not in content, "Git merge conflict markers still present in build.py"

    # Run the build script
    result = subprocess.run([sys.executable, build_path], capture_output=True, text=True)
    assert result.returncode == 0, f"build.py exited with code {result.returncode}. Output: {result.stdout}\n{result.stderr}"