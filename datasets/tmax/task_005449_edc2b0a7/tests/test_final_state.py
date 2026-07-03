# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_nginx_proxy_fixed():
    """
    Test that Nginx is running and proxying requests correctly.
    A request to http://127.0.0.1:9090/ should return 200 OK.
    """
    url = "http://127.0.0.1:9090/"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status_code = response.getcode()
            assert status_code == 200, f"Expected Nginx to return 200 OK, got {status_code}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Nginx returned HTTP error: {e.code}")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx at {url}. Is it running? Error: {e.reason}")
    except Exception as e:
        pytest.fail(f"Unexpected error when testing Nginx: {e}")

def test_classifier_script_exists():
    path = "/home/user/classifier.py"
    assert os.path.isfile(path), f"Classifier script not found at {path}"

def test_classifier_accuracy():
    """
    Test the classifier against the clean and evil corpora.
    Clean files should exit with 0.
    Evil files should exit with 1.
    """
    classifier_path = "/home/user/classifier.py"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isfile(classifier_path), f"Classifier script missing at {classifier_path}"
    assert os.path.isdir(clean_dir), f"Clean corpus missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus missing at {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "No files found in clean corpus directory."
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    failed_clean = []
    for clean_file in clean_files:
        result = subprocess.run(
            ["python3", classifier_path, clean_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            failed_clean.append(os.path.basename(clean_file))

    failed_evil = []
    for evil_file in evil_files:
        result = subprocess.run(
            ["python3", classifier_path, evil_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 1:
            failed_evil.append(os.path.basename(evil_file))

    error_messages = []
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))