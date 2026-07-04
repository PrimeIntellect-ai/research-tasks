# test_final_state.py

import os
import json
import glob
import subprocess
import urllib.request
import urllib.error
import pytest

BASE_DIR = "/home/user/telemetry-system"
URL = "http://127.0.0.1:8080/api/process"

def test_ci_script():
    ci_script = os.path.join(BASE_DIR, "ci.sh")
    assert os.path.isfile(ci_script), f"Missing CI script at {ci_script}"

    result = subprocess.run(["bash", ci_script], capture_output=True, text=True)
    assert result.returncode == 0, f"ci.sh failed with exit code {result.returncode}. Output:\n{result.stdout}\n{result.stderr}"
    assert "CI PASS" in result.stdout, f"ci.sh did not print 'CI PASS'. Output:\n{result.stdout}"

def test_adversarial_corpus():
    clean_dir = os.path.join(BASE_DIR, "corpus", "clean")
    evil_dir = os.path.join(BASE_DIR, "corpus", "evil")

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean corpus files found"
    assert len(evil_files) > 0, "No evil corpus files found"

    clean_failed = []
    evil_bypassed = []

    for c_file in clean_files:
        with open(c_file, 'rb') as f:
            data = f.read()
        req = urllib.request.Request(URL, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    clean_failed.append(os.path.basename(c_file))
        except urllib.error.HTTPError as e:
            clean_failed.append(os.path.basename(c_file))
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to {URL}: {e}")

    for e_file in evil_files:
        with open(e_file, 'rb') as f:
            data = f.read()
        req = urllib.request.Request(URL, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    evil_bypassed.append(os.path.basename(e_file))
        except urllib.error.HTTPError as e:
            if e.code != 400:
                evil_bypassed.append(os.path.basename(e_file))
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to {URL}: {e}")

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))