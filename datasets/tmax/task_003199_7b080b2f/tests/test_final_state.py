# test_final_state.py

import os
import sys
import subprocess
import importlib.util
import pytest
import re

def test_build_system():
    harness_dir = "/home/user/legacy_harness"
    tester_path = os.path.join(harness_dir, "tester")

    # Run cmake and make
    cmake_result = subprocess.run(["cmake", "."], cwd=harness_dir, capture_output=True, text=True)
    assert cmake_result.returncode == 0, f"cmake failed:\n{cmake_result.stderr}"

    make_result = subprocess.run(["make"], cwd=harness_dir, capture_output=True, text=True)
    assert make_result.returncode == 0, f"make failed:\n{make_result.stderr}"

    assert os.path.isfile(tester_path), f"tester executable not found at {tester_path}"
    assert os.access(tester_path, os.X_OK), f"tester at {tester_path} is not executable"

def test_adversarial_corpus():
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_path), f"Missing sanitizer script: {sanitizer_path}"

    # Dynamically import the sanitizer module
    spec = importlib.util.spec_from_file_location("sanitizer", sanitizer_path)
    sanitizer = importlib.util.module_from_spec(spec)
    sys.modules["sanitizer"] = sanitizer
    try:
        spec.loader.exec_module(sanitizer)
    except Exception as e:
        pytest.fail(f"Failed to load {sanitizer_path}: {e}")

    assert hasattr(sanitizer, "analyze_payload"), "analyze_payload function is missing"

    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    for f in evil_files:
        try:
            if sanitizer.analyze_payload(f) is not False:
                evil_bypassed.append(os.path.basename(f))
        except Exception as e:
            evil_bypassed.append(f"{os.path.basename(f)} (error: {e})")

    clean_modified = []
    for f in clean_files:
        try:
            if sanitizer.analyze_payload(f) is not True:
                clean_modified.append(os.path.basename(f))
        except Exception as e:
            clean_modified.append(f"{os.path.basename(f)} (error: {e})")

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_proxy_configuration():
    proxy_path = "/home/user/proxy.py"
    assert os.path.isfile(proxy_path), f"Missing proxy script: {proxy_path}"

    with open(proxy_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for required configurations
    assert "8080" in content, "Proxy script does not contain the listening port 8080"
    assert "9000" in content, "Proxy script does not contain the upstream port 9000"
    assert "X-QA-Auth" in content, "Proxy script does not contain the required header 'X-QA-Auth'"
    assert "Tango42" in content, "Proxy script does not contain the required header value 'Tango42'"