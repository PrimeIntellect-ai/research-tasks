# test_final_state.py

import os
import glob
import json
import urllib.request
import subprocess
import pytest

def test_cjson_compiled():
    so_path = "/app/cjson-1.7.15/libcjson.so"
    assert os.path.isfile(so_path), f"Expected shared library {so_path} does not exist. Did you fix the Makefile and compile it?"

def test_rest_api_running():
    url = "http://127.0.0.1:8080/limits"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode("utf-8"))
            assert data.get("max_cpu") == 100, f"Expected max_cpu=100, got {data.get('max_cpu')}"
            assert data.get("max_mem") == 200, f"Expected max_mem=200, got {data.get('max_mem')}"
    except Exception as e:
        pytest.fail(f"Failed to connect to REST API at {url} or parse its response: {e}")

def test_ci_validator_corpus():
    validator_bin = "/home/user/ci_validator"
    assert os.path.isfile(validator_bin), f"Validator binary {validator_bin} does not exist."
    assert os.access(validator_bin, os.X_OK), f"Validator binary {validator_bin} is not executable."

    clean_dir = "/home/user/corpus/clean"
    evil_dir = "/home/user/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for f in clean_files:
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "/app/cjson-1.7.15:" + env.get("LD_LIBRARY_PATH", "")
        res = subprocess.run([validator_bin, f], env=env, capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_bypassed = []
    for f in evil_files:
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "/app/cjson-1.7.15:" + env.get("LD_LIBRARY_PATH", "")
        res = subprocess.run([validator_bin, f], env=env, capture_output=True)
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(f))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_bypassed)}")

    if error_messages:
        pytest.fail("Corpus validation failed: " + " | ".join(error_messages))