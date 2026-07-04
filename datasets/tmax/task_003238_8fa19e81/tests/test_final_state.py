# test_final_state.py

import os
import json
import math
import urllib.request
import pytest

def test_c_program_exists():
    c_source = "/home/user/pipeline/process.c"
    binary = "/home/user/pipeline/process"

    assert os.path.isfile(c_source), f"C source file {c_source} is missing. You must write your code here."
    assert os.path.isfile(binary), f"Compiled binary {binary} is missing. Did you compile your C program?"
    assert os.access(binary, os.X_OK), f"File {binary} is not executable."

def test_report_json_file_exists():
    report_path = "/home/user/public_html/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing. Did you save the output?"

def test_web_server_and_report_content():
    url = "http://localhost:8080/report.json"
    try:
        response = urllib.request.urlopen(url, timeout=5)
        data = response.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to fetch {url}. Is the web server running on port 8080? Error: {e}")

    try:
        report = json.loads(data)
    except json.JSONDecodeError:
        pytest.fail("The served report.json is not valid JSON.")

    assert "sensor" in report, "Missing 'sensor' key in JSON."
    assert report["sensor"] == "S-100", f"Expected sensor 'S-100', got {report['sensor']}"

    assert "latest_zscores" in report, "Missing 'latest_zscores' key in JSON."
    assert "reference_distance" in report, "Missing 'reference_distance' key in JSON."

    # Recompute ground truth
    vals = [15.0, 14.0, 16.0, 15.0, 18.0]
    ref = [0.1, -0.2, 0.5, 1.0, -1.0]

    mean = sum(vals) / 5.0
    var = sum((v - mean) ** 2 for v in vals) / 5.0
    std = math.sqrt(var)

    expected_z = [(v - mean) / std for v in vals]
    expected_dist = math.sqrt(sum((expected_z[i] - ref[i]) ** 2 for i in range(5)))

    zscores = report["latest_zscores"]
    assert len(zscores) == 5, f"Expected 5 Z-scores, got {len(zscores)}"

    for i, (actual, expected) in enumerate(zip(zscores, expected_z)):
        assert math.isclose(actual, expected, abs_tol=1e-4), \
            f"Z-score at index {i} mismatch. Expected {expected:.5f}, got {actual}"

    actual_dist = report["reference_distance"]
    assert math.isclose(actual_dist, expected_dist, abs_tol=1e-4), \
        f"Reference distance mismatch. Expected {expected_dist:.5f}, got {actual_dist}"