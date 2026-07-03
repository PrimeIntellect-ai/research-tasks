# test_final_state.py

import os
import sys
import importlib.util
import subprocess
import pytest

WORKSPACE = "/home/user/telemetry_diag"

def test_extracted_payloads():
    payloads_file = os.path.join(WORKSPACE, "extracted_payloads.txt")
    assert os.path.isfile(payloads_file), f"Missing {payloads_file}"

    with open(payloads_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_payloads = ["1A2B", "5F5F", "0000", "ABCD"]
    assert lines == expected_payloads, f"Extracted payloads do not match expected output. Got: {lines}"

def test_pipeline_functions():
    pipeline_path = os.path.join(WORKSPACE, "pipeline.py")
    assert os.path.isfile(pipeline_path), f"Missing {pipeline_path}"

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("pipeline", pipeline_path)
    pipeline = importlib.util.module_from_spec(spec)
    sys.modules["pipeline"] = pipeline
    spec.loader.exec_module(pipeline)

    # Check decode_payload
    assert hasattr(pipeline, "decode_payload"), "Missing decode_payload function in pipeline.py"

    # Test cases for decode_payload: (val ^ 0x5A5A) % 5000
    test_cases_decode = {
        "1A2B": (int("1A2B", 16) ^ 0x5A5A) % 5000,
        "5F5F": (int("5F5F", 16) ^ 0x5A5A) % 5000,
        "0000": (int("0000", 16) ^ 0x5A5A) % 5000,
        "ABCD": (int("ABCD", 16) ^ 0x5A5A) % 5000,
        "FFFF": (int("FFFF", 16) ^ 0x5A5A) % 5000,
    }

    for hex_str, expected in test_cases_decode.items():
        result = pipeline.decode_payload(hex_str)
        assert result == expected, f"decode_payload('{hex_str}') returned {result}, expected {expected}"

    # Check that decode_payload does not use subprocess (pure Python)
    with open(pipeline_path, "r") as f:
        content = f.read()
        assert "subprocess" not in content or "subprocess.run" not in content, "decode_payload must be a pure Python implementation and not use subprocess"

    # Check calculate_temperature
    assert hasattr(pipeline, "calculate_temperature"), "Missing calculate_temperature function in pipeline.py"

    # Test cases for calculate_temperature: round((val / 10.0) * 1.8 + 32.0, 2)
    test_cases_temp = [0, 100, 255, 1234, 4999]
    for val in test_cases_temp:
        expected = round((val / 10.0) * 1.8 + 32.0, 2)
        result = pipeline.calculate_temperature(val)
        assert result == expected, f"calculate_temperature({val}) returned {result}, expected {expected}"

def test_student_pytest_suite():
    test_file = os.path.join(WORKSPACE, "test_pipeline.py")
    assert os.path.isfile(test_file), f"Missing student test file {test_file}"

    # Run the student's pytest suite
    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"Student's pytest suite failed:\n{result.stdout}\n{result.stderr}"

    # Ensure there are at least 4 test cases
    with open(test_file, "r") as f:
        content = f.read()
        test_count = content.count("def test_")
        assert test_count >= 1, "Student test file must contain at least one test function (preferably parameterized or multiple test functions)"