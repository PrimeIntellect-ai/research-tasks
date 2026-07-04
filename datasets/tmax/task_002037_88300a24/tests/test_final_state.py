# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import math
import xml.etree.ElementTree as ET
import pytest

def test_shared_libraries_exist():
    lib1 = '/home/user/libs/libmathops.so.1.0.0'
    lib2 = '/home/user/libs/libmathops.so.2.1.0'

    assert os.path.isfile(lib1), f"Shared library {lib1} is missing."
    assert os.path.isfile(lib2), f"Shared library {lib2} is missing."

    with open(lib1, 'rb') as f:
        assert f.read(4) == b'\x7fELF', f"{lib1} is not a valid ELF file."
    with open(lib2, 'rb') as f:
        assert f.read(4) == b'\x7fELF', f"{lib2} is not a valid ELF file."

def test_deployment_summary():
    summary_path = '/home/user/deployment_summary.json'
    assert os.path.isfile(summary_path), f"File {summary_path} is missing."

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON.")

    assert data.get("selected_version") == "2.1.0", "Incorrect selected_version in deployment_summary.json."
    assert data.get("library_path") == "/home/user/libs/libmathops.so.2.1.0", "Incorrect library_path in deployment_summary.json."
    assert data.get("api_port") == 8080, "Incorrect api_port in deployment_summary.json."

def test_api_running_and_correct():
    url = 'http://127.0.0.1:8080/api/trajectory'
    payload = json.dumps({"v": 10.0, "theta": math.pi / 4}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"API returned status {response.status}"
            resp_data = json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to API on port 8080: {e}")

    assert "distance" in resp_data, "Response missing 'distance' key."
    assert "version_used" in resp_data, "Response missing 'version_used' key."

    assert resp_data["version_used"] == "2.1.0", "API returned incorrect version_used."

    # Expected distance for v2: ((10.0^2 * sin(2 * pi/4)) / 9.81) * 0.95
    expected_distance = ((100.0 * math.sin(2.0 * math.pi / 4)) / 9.81) * 0.95
    assert math.isclose(resp_data["distance"], expected_distance, rel_tol=1e-4), \
        f"API returned incorrect distance. Expected ~{expected_distance}, got {resp_data['distance']}"

def test_test_results_xml():
    xml_path = '/home/user/test_results.xml'
    assert os.path.isfile(xml_path), f"File {xml_path} is missing."

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError:
        pytest.fail(f"File {xml_path} is not valid XML.")

    # Check if there are test cases and they passed
    testcases = list(root.iter('testcase'))
    assert len(testcases) > 0, "No test cases found in test_results.xml."

    failures = list(root.iter('failure'))
    errors = list(root.iter('error'))
    assert len(failures) == 0 and len(errors) == 0, "There are failing tests in test_results.xml."