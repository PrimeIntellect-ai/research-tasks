# test_final_state.py

import os
import subprocess
import json
import urllib.request
import time
import shutil
import pytest

def test_detector_corpus():
    detector_script = "/home/user/detector.py"
    assert os.path.isfile(detector_script), f"Detector script missing at {detector_script}"

    clean_dir = "/home/user/test_data/clean/"
    evil_dir = "/home/user/test_data/evil/"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(".csv")]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(".csv")]

    assert len(clean_files) > 0, "No clean test files found."
    assert len(evil_files) > 0, "No evil test files found."

    clean_failures = []
    for f in clean_files:
        result = subprocess.run(["python3", detector_script, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run(["python3", detector_script, f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    assert not error_messages, " | ".join(error_messages)

def test_pipeline_e2e():
    # Verify services are listening
    try:
        urllib.request.urlopen("http://localhost:5000/", timeout=2)
    except Exception as e:
        # It might return 404 for root, but connection should succeed
        if isinstance(e, urllib.error.HTTPError):
            pass
        else:
            pytest.fail(f"Flask API does not seem to be running on port 5000: {e}")

    # Prepare test files for the pipeline
    clean_src = [os.path.join("/home/user/test_data/clean", f) for f in os.listdir("/home/user/test_data/clean") if f.endswith(".csv")][0]
    evil_src = [os.path.join("/home/user/test_data/evil", f) for f in os.listdir("/home/user/test_data/evil") if f.endswith(".csv")][0]

    # Create temporary copies so we don't permanently delete test data
    tmp_clean = "/tmp/pipeline_clean_test.csv"
    tmp_evil = "/tmp/pipeline_evil_test.csv"
    shutil.copy(clean_src, tmp_clean)
    shutil.copy(evil_src, tmp_evil)

    def post_file(file_path):
        req = urllib.request.Request(
            "http://localhost:5000/process",
            data=json.dumps({"file_path": file_path}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status
        except urllib.error.HTTPError as e:
            return e.code
        except Exception as e:
            pytest.fail(f"Failed to POST to API: {e}")

    # Process clean file
    status_clean = post_file(tmp_clean)
    assert status_clean in (200, 202), f"Expected 200/202 from API, got {status_clean}"

    # Process evil file
    status_evil = post_file(tmp_evil)
    assert status_evil in (200, 202), f"Expected 200/202 from API, got {status_evil}"

    # Wait for async worker to process
    accepted_path = f"/home/user/accepted/{os.path.basename(tmp_clean)}"
    rejected_path = f"/home/user/rejected/{os.path.basename(tmp_evil)}"

    timeout = 10
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(accepted_path) and os.path.exists(rejected_path):
            break
        time.sleep(0.5)

    assert os.path.exists(accepted_path), f"Clean file was not moved to {accepted_path} by the worker."
    assert os.path.exists(rejected_path), f"Evil file was not moved to {rejected_path} by the worker."

    # Cleanup
    if os.path.exists(accepted_path):
        os.remove(accepted_path)
    if os.path.exists(rejected_path):
        os.remove(rejected_path)