# test_final_state.py

import os
import subprocess
import tempfile
import urllib.request
import json
import pytest

CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"
RUST_PROJECT_DIR = "/home/user/sequence_filter"

def test_services_running():
    # Check if ports 6379, 5000, 3000 are listening
    import socket
    for port in [6379, 5000, 3000]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            assert s.connect_ex(('127.0.0.1', port)) == 0, f"Service on port {port} is not running"

def test_flask_baseline_score():
    try:
        req = urllib.request.Request("http://127.0.0.1:5000/baseline_score")
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            assert "4.25" in data or float(data) == 4.25, f"Expected baseline score 4.25, got {data}"
    except Exception as e:
        pytest.fail(f"Failed to fetch baseline score from Flask: {e}")

def test_clean_corpus_preserved():
    with tempfile.TemporaryDirectory() as out_dir:
        cmd = ["cargo", "run", "--release", "--", CLEAN_CORPUS_DIR, out_dir]
        result = subprocess.run(cmd, cwd=RUST_PROJECT_DIR, capture_output=True, text=True)
        assert result.returncode == 0, f"Cargo run failed for clean corpus:\n{result.stderr}"

        clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".fasta")]
        out_files = [f for f in os.listdir(out_dir) if f.endswith(".fasta")]

        missing = set(clean_files) - set(out_files)
        assert not missing, f"{len(missing)} of {len(clean_files)} clean modified/rejected. Missing: {list(missing)[:5]}"

def test_evil_corpus_rejected():
    with tempfile.TemporaryDirectory() as out_dir:
        cmd = ["cargo", "run", "--release", "--", EVIL_CORPUS_DIR, out_dir]
        result = subprocess.run(cmd, cwd=RUST_PROJECT_DIR, capture_output=True, text=True)
        assert result.returncode == 0, f"Cargo run failed for evil corpus:\n{result.stderr}"

        evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".fasta")]
        out_files = [f for f in os.listdir(out_dir) if f.endswith(".fasta")]

        bypassed = set(out_files)
        assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed. Bypassed: {list(bypassed)[:5]}"

def test_verification_log_exists():
    assert os.path.isfile("/home/user/verification.log"), "/home/user/verification.log is missing"