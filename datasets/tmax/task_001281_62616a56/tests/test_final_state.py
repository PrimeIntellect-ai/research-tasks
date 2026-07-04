# test_final_state.py

import os
import time
import subprocess
import csv
import urllib.request
import json
import pytest

def test_phase1_pipeline_restoration():
    # Check config.ini changes
    config_path = "/app/config.ini"
    assert os.path.isfile(config_path), f"{config_path} is missing."
    with open(config_path, "r") as f:
        config_content = f.read()

    assert "port = 6379" in config_content or "port=6379" in config_content, "Redis port in config.ini is not set to 6379."
    assert "queue_name = log_queue" in config_content or "queue_name=log_queue" in config_content, "queue_name in config.ini is not set to log_queue."

    # Test End-to-End flow
    test_string = "verification_test_string_" + str(time.time())
    data = json.dumps({"log": test_string}).encode('utf-8')
    req = urllib.request.Request("http://localhost:8080/ingest", data=data, headers={'Content-Type': 'application/json'})

    try:
        response = urllib.request.urlopen(req, timeout=5)
        assert response.status == 200, f"API returned status code {response.status}"
    except Exception as e:
        pytest.fail(f"Failed to send request to API: {e}")

    time.sleep(2)

    processed_log_path = "/app/processed.log"
    assert os.path.isfile(processed_log_path), f"{processed_log_path} was not created."

    with open(processed_log_path, "r") as f:
        processed_content = f.read()

    assert test_string in processed_content, f"Test string '{test_string}' was not found in {processed_log_path}. Pipeline is not processing logs correctly."

def test_phase2_parser_fixed():
    parser_path = "/home/user/log_parser_repo/parser.py"
    assert os.path.isfile(parser_path), f"{parser_path} is missing."
    with open(parser_path, "r") as f:
        content = f.read()

    assert "non_existent_module" not in content, "The bad import 'non_existent_module' is still in parser.py."

    # Try to import and use the installed package
    try:
        import sys
        # Assuming the package is installed in the system environment, we can try to run a python snippet
        # Or we can just run a subprocess to test the system python environment
        code = """
import parser
res1 = parser.parse('{"msg": "modern"}')
res2 = parser.parse('{"msg": "\\"legacy format\\""}')
print("OK")
"""
        result = subprocess.run(["python3", "-c", code], capture_output=True, text=True)
        assert "OK" in result.stdout and result.returncode == 0, f"Parser failed to handle both modern and legacy logs. Error: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Failed to test parser module: {e}")

def test_phase3_security_detector():
    detector_script = "/home/user/detector.py"
    assert os.path.isfile(detector_script), f"{detector_script} is missing."

    clean_dir = "/var/opt/verifier/clean"
    evil_dir = "/var/opt/verifier/evil"
    clean_csv = "/tmp/clean_results.csv"
    evil_csv = "/tmp/evil_results.csv"

    # Run detector on clean corpus
    res_clean = subprocess.run(["python3", detector_script, clean_dir, clean_csv], capture_output=True, text=True)
    assert res_clean.returncode == 0, f"Detector script failed on clean corpus: {res_clean.stderr}"
    assert os.path.isfile(clean_csv), f"Detector script did not produce {clean_csv}"

    # Run detector on evil corpus
    res_evil = subprocess.run(["python3", detector_script, evil_dir, evil_csv], capture_output=True, text=True)
    assert res_evil.returncode == 0, f"Detector script failed on evil corpus: {res_evil.stderr}"
    assert os.path.isfile(evil_csv), f"Detector script did not produce {evil_csv}"

    # Verify Clean Corpus (Expected: ACCEPT)
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.log')]
    clean_results = {}
    with open(clean_csv, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                clean_results[row[0]] = row[1].strip().upper()

    clean_modified = []
    for cf in clean_files:
        if clean_results.get(cf) != "ACCEPT":
            clean_modified.append(cf)

    # Verify Evil Corpus (Expected: REJECT)
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.log')]
    evil_results = {}
    with open(evil_csv, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                evil_results[row[0]] = row[1].strip().upper()

    evil_bypassed = []
    for ef in evil_files:
        if evil_results.get(ef) != "REJECT":
            evil_bypassed.append(ef)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))