# test_final_state.py

import os
import json
import tarfile
import subprocess
import re

def test_makefile_fixed_and_binary_compiled():
    # Check if Makefile was fixed (should have -lm)
    makefile_path = "/home/user/mathtool/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} is missing."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-lm" in content, "Makefile does not link the math library (-lm)."

    # Check if mathtool binary exists
    binary_path = "/home/user/mathtool/mathtool"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

    # Check if it links to libm
    ldd_output = subprocess.check_output(["ldd", binary_path], text=True)
    assert "libm.so" in ldd_output, "mathtool binary is not linked to libm."

def test_parser_c_fixed():
    parser_path = "/home/user/mathtool/src/parser.c"
    assert os.path.isfile(parser_path), f"{parser_path} is missing."
    with open(parser_path, "r") as f:
        content = f.read()

    # Check for allocation size fix
    assert re.search(r"malloc\s*\(\s*len\s*\+\s*1\s*\)", content), "parser.c does not allocate len + 1 bytes."
    # Check for null termination
    assert re.search(r"buf\s*\[\s*len\s*\]\s*=\s*['\"]\\[0o]0?['\"]", content), "parser.c does not null-terminate the buffer."

def test_fixture_json():
    fixture_path = "/home/user/mathtool/tests/fixture.json"
    assert os.path.isfile(fixture_path), f"{fixture_path} is missing."
    with open(fixture_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{fixture_path} is not valid JSON."

    assert isinstance(data, list), "Fixture should be a JSON array."
    assert len(data) == 3, "Fixture should contain exactly 3 test cases."

    expected_cases = [
        {"expression": "3 + 5 * 2", "expected": 13.0},
        {"expression": "pow(2, 3) - 1", "expected": 7.0},
        {"expression": "10.0005 + 0.0005", "expected": 10.001}
    ]

    for case in expected_cases:
        assert case in data, f"Missing expected test case in fixture: {case}"

def test_test_report_json():
    report_path = "/home/user/mathtool/test_report.json"
    assert os.path.isfile(report_path), f"{report_path} is missing."
    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} is not valid JSON."

    assert data.get("total") == 3, "Test report 'total' should be 3."
    assert data.get("passed") == 3, "Test report 'passed' should be 3."
    assert data.get("failed") == 0, "Test report 'failed' should be 0."

def test_artifact_packaging():
    tar_path = "/home/user/artifact.tar.gz"
    assert os.path.isfile(tar_path), f"{tar_path} is missing."

    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar archive."

    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getnames()

    assert len(members) == 2, f"Archive should contain exactly 2 files, found: {members}"
    assert "mathtool" in members, "Archive is missing 'mathtool'."
    assert "test_report.json" in members, "Archive is missing 'test_report.json'."