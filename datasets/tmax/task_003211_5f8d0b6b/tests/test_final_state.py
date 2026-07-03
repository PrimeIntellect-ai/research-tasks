# test_final_state.py

import os
import subprocess
import math

def test_distance_result_created_and_correct():
    result_file = "/home/user/distance_result.txt"
    assert os.path.isfile(result_file), f"Expected result file {result_file} is missing."

    with open(result_file, "r") as f:
        content = f.read().strip()

    try:
        distance = float(content)
    except ValueError:
        assert False, f"Content of {result_file} is not a valid float: {content}"

    expected_distance = 1.258650070512211e-07
    assert math.isclose(distance, expected_distance, rel_tol=1e-5), \
        f"Distance {distance} does not match expected float64 precision distance ~{expected_distance}. " \
        "Did you correctly update to float64?"

def test_parser_uses_float64():
    parser_path = "/home/user/telemetry/parser.go"
    assert os.path.isfile(parser_path), f"File {parser_path} is missing."

    with open(parser_path, "r") as f:
        content = f.read()

    assert "float64" in content, "The parser.go file must use float64."
    assert "float32" not in content, "All instances of float32 should be removed from parser.go."

def test_fuzz_test_exists():
    test_path = "/home/user/telemetry/parser_test.go"
    assert os.path.isfile(test_path), f"Fuzz test file {test_path} is missing."

    with open(test_path, "r") as f:
        content = f.read()

    assert "FuzzParseLine" in content, "The FuzzParseLine function is missing in parser_test.go."

def test_go_test_passes():
    try:
        result = subprocess.run(
            ["go", "test"],
            cwd="/home/user/telemetry",
            capture_output=True,
            text=True,
            timeout=15
        )
        assert result.returncode == 0, f"'go test' failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except FileNotFoundError:
        assert False, "The 'go' command was not found."

def test_verify_go_exists():
    verify_path = "/home/user/verify.go"
    assert os.path.isfile(verify_path), f"The script {verify_path} is missing."