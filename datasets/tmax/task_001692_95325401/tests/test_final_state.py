# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import subprocess
import pytest

def test_services_running_and_routing():
    """Test that Nginx, Backend, and Redis are running and correctly routed."""
    url = "http://127.0.0.1:8080/api/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = response.read().decode('utf-8')
            try:
                json_data = json.loads(data)
            except json.JSONDecodeError:
                pytest.fail(f"Response is not valid JSON: {data}")

            assert json_data.get("status") == "ok", f"Expected status 'ok', got {json_data.get('status')}"
            assert json_data.get("redis") == "connected", f"Expected redis 'connected', got {json_data.get('redis')}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 or backend routing failed: {e}")

def test_cracked_pin():
    """Test that the cracked PIN is exactly 4815."""
    pin_file = "/home/user/cracked_pin.txt"
    assert os.path.isfile(pin_file), f"Cracked PIN file missing at {pin_file}"

    with open(pin_file, "r") as f:
        pin = f.read().strip()

    assert pin == "4815", f"Expected PIN '4815', but got '{pin}'"

def test_detector_compilation_and_classification():
    """Test compiling the Rust detector and classifying the adversarial corpora."""
    detector_dir = "/home/user/detector"
    assert os.path.isdir(detector_dir), f"Detector project directory missing at {detector_dir}"

    cargo_toml = os.path.join(detector_dir, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml missing in {detector_dir}"

    # Compile the detector
    build_proc = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=detector_dir,
        capture_output=True,
        text=True
    )
    assert build_proc.returncode == 0, f"Failed to compile detector:\nSTDOUT:\n{build_proc.stdout}\nSTDERR:\n{build_proc.stderr}"

    detector_bin = os.path.join(detector_dir, "target", "release", "detector")
    assert os.path.isfile(detector_bin), f"Compiled detector binary missing at {detector_bin}"
    assert os.access(detector_bin, os.X_OK), f"Detector binary at {detector_bin} is not executable"

    # Test Evil Corpus
    evil_corpus_dir = "/app/verifier/corpus/evil"
    assert os.path.isdir(evil_corpus_dir), f"Evil corpus directory missing at {evil_corpus_dir}"
    evil_files = {f for f in os.listdir(evil_corpus_dir) if f.endswith('.txt')}

    evil_proc = subprocess.run(
        [detector_bin, evil_corpus_dir],
        capture_output=True,
        text=True
    )
    assert evil_proc.returncode == 0, f"Detector failed on evil corpus:\n{evil_proc.stderr}"

    evil_output = evil_proc.stdout.strip().splitlines()
    evil_bypassed = []
    for f in evil_files:
        expected_line = f"[MALICIOUS] {f}"
        if expected_line not in evil_output:
            evil_bypassed.append(f)

    # Test Clean Corpus
    clean_corpus_dir = "/app/verifier/corpus/clean"
    assert os.path.isdir(clean_corpus_dir), f"Clean corpus directory missing at {clean_corpus_dir}"
    clean_files = {f for f in os.listdir(clean_corpus_dir) if f.endswith('.txt')}

    clean_proc = subprocess.run(
        [detector_bin, clean_corpus_dir],
        capture_output=True,
        text=True
    )
    assert clean_proc.returncode == 0, f"Detector failed on clean corpus:\n{clean_proc.stderr}"

    clean_output = clean_proc.stdout.strip().splitlines()
    clean_modified = []
    for f in clean_files:
        expected_line = f"[CLEAN] {f}"
        if expected_line not in clean_output:
            clean_modified.append(f)

    # Surface clear summary on failure
    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))