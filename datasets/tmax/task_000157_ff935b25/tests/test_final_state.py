# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import glob
import pytest

def test_frame42_checksum():
    checksum_file = "/home/user/frame42_checksum.txt"
    assert os.path.isfile(checksum_file), f"Checksum file {checksum_file} is missing."
    with open(checksum_file, "r") as f:
        content = f.read().strip()
    assert "0x4F8A2B9C" in content, f"Expected checksum '0x4F8A2B9C' not found in {checksum_file}. Content: {content}"

def test_detector_clean_corpus():
    detector_script = "/home/user/detector.sh"
    assert os.path.isfile(detector_script), f"Detector script {detector_script} is missing."
    assert os.access(detector_script, os.X_OK), f"Detector script {detector_script} is not executable."

    clean_files = glob.glob("/home/user/corpora/clean/*")
    assert len(clean_files) > 0, "Clean corpus is empty."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([detector_script, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected by detector.sh. Offending files: {failed_files}"

def test_detector_evil_corpus():
    detector_script = "/home/user/detector.sh"
    assert os.path.isfile(detector_script), f"Detector script {detector_script} is missing."
    assert os.access(detector_script, os.X_OK), f"Detector script {detector_script} is not executable."

    evil_files = glob.glob("/home/user/corpora/evil/*")
    assert len(evil_files) > 0, "Evil corpus is empty."

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([detector_script, filepath], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(filepath))

    assert len(bypassed_files) == 0, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed detector.sh. Offending files: {bypassed_files}"

def test_proxy_clean_corpus():
    clean_files = glob.glob("/home/user/corpora/clean/*")
    assert len(clean_files) > 0, "Clean corpus is empty."

    failed_files = []
    for filepath in clean_files:
        with open(filepath, "rb") as f:
            data = f.read()

        req = urllib.request.Request("http://localhost:8080/validate", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status != 200:
                    failed_files.append(os.path.basename(filepath))
        except urllib.error.HTTPError as e:
            if e.code != 200:
                failed_files.append(os.path.basename(filepath))
        except Exception as e:
            failed_files.append(os.path.basename(filepath))

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected by proxy. Offending files: {failed_files}"

def test_proxy_evil_corpus():
    evil_files = glob.glob("/home/user/corpora/evil/*")
    assert len(evil_files) > 0, "Evil corpus is empty."

    bypassed_files = []
    for filepath in evil_files:
        with open(filepath, "rb") as f:
            data = f.read()

        req = urllib.request.Request("http://localhost:8080/validate", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    bypassed_files.append(os.path.basename(filepath))
        except urllib.error.HTTPError as e:
            if e.code != 400:
                bypassed_files.append(os.path.basename(filepath))
        except Exception as e:
            # If it fails with something other than HTTPError (like connection refused), we should probably count it as a failure to return 400 properly
            bypassed_files.append(os.path.basename(filepath))

    assert len(bypassed_files) == 0, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed proxy. Offending files: {bypassed_files}"