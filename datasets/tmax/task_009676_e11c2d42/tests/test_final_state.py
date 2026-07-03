# test_final_state.py
import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/router_project"

def test_makefile_fixed():
    makefile_path = os.path.join(PROJECT_DIR, "Makefile")
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}."

    with open(makefile_path, "r") as f:
        lines = f.readlines()

    # Check if there is a line starting with a tab that contains 'gcc'
    has_tab_gcc = any(line.startswith("\t") and "gcc" in line for line in lines)
    assert has_tab_gcc, "Makefile was not fixed to use tabs for the gcc build command."

def test_executable_built():
    exe_path = os.path.join(PROJECT_DIR, "url_router")
    assert os.path.isfile(exe_path), f"url_router executable was not found at {exe_path}."
    assert os.access(exe_path, os.X_OK), f"url_router at {exe_path} is not executable."

def test_report_json_exists_and_valid():
    report_path = os.path.join(PROJECT_DIR, "report.json")
    assert os.path.isfile(report_path), f"report.json was not generated at {report_path}."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json does not contain valid JSON.")

    assert "total_tested" in data, "Missing 'total_tested' key in report.json."
    assert "successful_executions" in data, "Missing 'successful_executions' key in report.json."
    assert "results" in data, "Missing 'results' key in report.json."

    assert data["total_tested"] == 4, f"Expected total_tested to be 4, got {data['total_tested']}."
    assert data["successful_executions"] == 4, f"Expected successful_executions to be 4, got {data['successful_executions']}."

    results = data["results"]
    assert isinstance(results, list), "'results' must be a list."
    assert len(results) == 4, f"Expected 4 results in the list, got {len(results)}."

    expected_results = [
        {"original_url": "/api/v1/users?id=10&active=true", "parsed_route": "/api/v1/users", "parsed_params": "id=10&active=true"},
        {"original_url": "/api/v1/status", "parsed_route": "/api/v1/status", "parsed_params": "none"},
        {"original_url": "/home?user=admin", "parsed_route": "/home", "parsed_params": "user=admin"},
        {"original_url": "/about", "parsed_route": "/about", "parsed_params": "none"}
    ]

    for i, expected in enumerate(expected_results):
        actual = results[i]
        assert actual.get("original_url") == expected["original_url"], f"Result {i} original_url mismatch. Expected '{expected['original_url']}', got '{actual.get('original_url')}'."
        assert actual.get("parsed_route") == expected["parsed_route"], f"Result {i} parsed_route mismatch. Expected '{expected['parsed_route']}', got '{actual.get('parsed_route')}'."
        assert actual.get("parsed_params") == expected["parsed_params"], f"Result {i} parsed_params mismatch. Expected '{expected['parsed_params']}', got '{actual.get('parsed_params')}'."

def test_router_c_fixed_behavior():
    exe_path = os.path.join(PROJECT_DIR, "url_router")
    if not os.path.isfile(exe_path):
        pytest.skip("url_router executable is missing, cannot test behavior.")

    # Test a URL without query params (which previously caused a segfault)
    try:
        result = subprocess.run([exe_path, "/api/v1/status"], capture_output=True, text=True, timeout=2)
    except subprocess.TimeoutExpired:
        pytest.fail("url_router execution timed out.")

    assert result.returncode == 0, f"url_router crashed or returned non-zero exit code on URL without query params (returncode: {result.returncode})."

    expected_output = "ROUTE:/api/v1/status|PARAMS:none|VALID:1"
    assert expected_output in result.stdout, f"url_router output is incorrect for URL without query params. Expected to find '{expected_output}', got '{result.stdout.strip()}'."