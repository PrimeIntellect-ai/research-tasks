# test_final_state.py

import os
import json
import pytest

def test_waf_analyzer_exists():
    script_path = "/home/user/waf_analyzer.py"
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist. Please create it."

def test_vulnerabilities_json_exists_and_valid():
    output_path = "/home/user/vulnerabilities.json"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did the script run and generate it?"

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} does not contain valid JSON.")

    assert isinstance(data, dict), f"The root of {output_path} must be a JSON object (dictionary)."

def test_vulnerabilities_json_content():
    output_path = "/home/user/vulnerabilities.json"
    if not os.path.isfile(output_path):
        pytest.skip(f"{output_path} missing.")

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Invalid JSON.")

    # Check Auth_Bypass
    assert "Auth_Bypass" in data, "Rule 'Auth_Bypass' is missing from the output."
    auth = data["Auth_Bypass"]
    assert auth.get("affected_package") == "auth_lib", "Auth_Bypass affected_package is incorrect."
    assert auth.get("installed_version") == "2.1.4", "Auth_Bypass installed_version is incorrect."
    assert auth.get("is_vulnerable") is True, "Auth_Bypass should be vulnerable."

    # Check Parser_Crash
    assert "Parser_Crash" in data, "Rule 'Parser_Crash' is missing from the output."
    parser = data["Parser_Crash"]
    assert parser.get("affected_package") == "parser_core", "Parser_Crash affected_package is incorrect."
    assert parser.get("installed_version") == "1.5.0", "Parser_Crash installed_version is incorrect."
    assert parser.get("is_vulnerable") is False, "Parser_Crash should NOT be vulnerable."

    # Check Data_Leak
    assert "Data_Leak" in data, "Rule 'Data_Leak' is missing from the output."
    data_leak = data["Data_Leak"]
    assert data_leak.get("affected_package") == "data_utils", "Data_Leak affected_package is incorrect."
    assert data_leak.get("installed_version") == "0.9.5", "Data_Leak installed_version is incorrect."
    assert data_leak.get("is_vulnerable") is True, "Data_Leak should be vulnerable."