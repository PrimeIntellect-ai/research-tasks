# test_final_state.py
import os
import json
import subprocess
import pytest

def test_scripts_exist():
    assert os.path.isfile("/home/user/protein_analysis.py"), "The script /home/user/protein_analysis.py is missing."
    assert os.path.isfile("/home/user/test_protein_analysis.py"), "The test script /home/user/test_protein_analysis.py is missing."

def test_outputs_exist():
    assert os.path.isfile("/home/user/output/gamma_params.json"), "The output JSON /home/user/output/gamma_params.json is missing."
    assert os.path.isfile("/home/user/output/distance_distribution.png"), "The output plot /home/user/output/distance_distribution.png is missing."

def test_json_content():
    json_path = "/home/user/output/gamma_params.json"
    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} is not valid JSON.")

    expected_keys = {"a", "loc", "scale"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, but got {set(data.keys())}."

    for key in expected_keys:
        assert isinstance(data[key], (int, float)), f"The value for '{key}' must be a number, but got {type(data[key])}."

def test_student_pytest_passes():
    test_file = "/home/user/test_protein_analysis.py"
    result = subprocess.run(
        ["pytest", test_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"Running pytest on {test_file} failed.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_student_test_file_content():
    test_file = "/home/user/test_protein_analysis.py"
    with open(test_file, "r") as f:
        content = f.read()

    assert "test_distance_computation" in content, "The test file must contain 'test_distance_computation'."
    assert "test_gamma_fit" in content, "The test file must contain 'test_gamma_fit'."