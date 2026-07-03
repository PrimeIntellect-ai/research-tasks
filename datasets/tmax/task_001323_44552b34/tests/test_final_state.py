# test_final_state.py

import os
import subprocess
import socket
import pytest

def test_config_updated():
    config_path = "/app/config.env"
    assert os.path.isfile(config_path), f"File {config_path} is missing"

    with open(config_path, "r") as f:
        content = f.read()

    assert "MODEL_PORT=8001" in content, "MODEL_PORT is not set to 8001 in config.env"
    assert "VECTOR_PORT=8002" in content, "VECTOR_PORT is not set to 8002 in config.env"
    assert "DIMENSIONS=10" in content, "DIMENSIONS is not set to 10 in config.env"

def test_services_running():
    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(('127.0.0.1', port)) == 0

    assert is_port_open(8001), "Embedding service is not listening on port 8001"
    assert is_port_open(8002), "Vector DB is not listening on port 8002"

def test_filter_script_exists_and_executable():
    script_path = "/home/user/filter.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_clean_corpus_accepted():
    clean_dir = "/home/user/corpora/clean"
    script_path = "/home/user/filter.sh"

    assert os.path.isdir(clean_dir), f"{clean_dir} directory is missing"

    failed_files = []
    total = 0

    for fname in sorted(os.listdir(clean_dir)):
        if fname.endswith(".json"):
            total += 1
            fpath = os.path.join(clean_dir, fname)
            result = subprocess.run([script_path, fpath], capture_output=True)
            if result.returncode != 0:
                failed_files.append(fname)

    assert total > 0, f"No JSON files found in {clean_dir}"
    assert len(failed_files) == 0, f"{len(failed_files)} of {total} clean modified (rejected instead of accepted). Offending files: {', '.join(failed_files)}"

def test_evil_corpus_rejected():
    evil_dir = "/home/user/corpora/evil"
    script_path = "/home/user/filter.sh"

    assert os.path.isdir(evil_dir), f"{evil_dir} directory is missing"

    failed_files = []
    total = 0

    for fname in sorted(os.listdir(evil_dir)):
        if fname.endswith(".json"):
            total += 1
            fpath = os.path.join(evil_dir, fname)
            result = subprocess.run([script_path, fpath], capture_output=True)
            # The script MUST exit with code 1 for evil files
            if result.returncode != 1:
                failed_files.append(fname)

    assert total > 0, f"No JSON files found in {evil_dir}"
    assert len(failed_files) == 0, f"{len(failed_files)} of {total} evil bypassed (accepted or crashed instead of rejected with code 1). Offending files: {', '.join(failed_files)}"