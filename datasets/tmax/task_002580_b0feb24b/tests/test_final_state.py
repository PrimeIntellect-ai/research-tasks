# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_end_to_end_proxy():
    """
    Test that the Nginx proxy is correctly configured and routes to the C backend.
    A clean HTTP POST request to http://127.0.0.1:8080/process should successfully
    return a 200 OK and "PROCESSED".
    """
    url = "http://127.0.0.1:8080/process"
    data = b"clean data"
    req = urllib.request.Request(url, data=data, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
            body = response.read().decode('utf-8', errors='ignore')
    except urllib.error.HTTPError as e:
        pytest.fail(f"End-to-end request failed with HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        pytest.fail(f"End-to-end request failed to connect: {e.reason}")
    except Exception as e:
        pytest.fail(f"End-to-end request encountered an unexpected error: {e}")

    assert status == 200, f"Expected HTTP status 200, got {status}"
    assert "PROCESSED" in body, f"Expected 'PROCESSED' in response body, got: {body}"

def test_detector_exists_and_executable():
    """
    Ensure the detector binary was compiled and is executable.
    """
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector binary not found at {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector at {detector_path} is not executable"

def test_detector_evil_corpus():
    """
    Ensure the detector rejects 100% of the evil corpus by returning exit code 1.
    """
    detector_path = "/home/user/detector"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run([detector_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}")

def test_detector_clean_corpus():
    """
    Ensure the detector accepts 100% of the clean corpus by returning exit code 0.
    """
    detector_path = "/home/user/detector"
    clean_dir = "/app/corpus/clean"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory."

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run([detector_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")