# test_final_state.py

import os
import subprocess
import configparser
import pytest
import urllib.request
import urllib.error

FILTER_BIN = "/home/user/archive_filter"
CLEAN_CORPUS_DIR = "/app/verifier_corpus/clean/"
EVIL_CORPUS_DIR = "/app/verifier_corpus/evil/"
CONFIG_PATH = "/app/flask_app/config.ini"

def test_filter_binary_exists_and_executable():
    assert os.path.isfile(FILTER_BIN), f"Filter binary {FILTER_BIN} does not exist."
    assert os.access(FILTER_BIN, os.X_OK), f"Filter binary {FILTER_BIN} is not executable."

def test_filter_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.skip("Clean corpus directory not found.")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    failed_files = []

    for f in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, f)
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(f)

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(clean_files)} clean files rejected (expected exit 0). Offending files: {failed_files}"

def test_filter_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.skip("Evil corpus directory not found.")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    failed_files = []

    for f in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, f)
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(f)

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected exit 1). Offending files: {failed_files}"

def test_config_updated():
    assert os.path.isfile(CONFIG_PATH), f"Config file {CONFIG_PATH} does not exist."
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    assert 'Upload' in config, "[Upload] section missing in config.ini"
    assert 'FILTER_CMD' in config['Upload'], "FILTER_CMD missing in config.ini"
    assert config['Upload']['FILTER_CMD'] == FILTER_BIN, f"FILTER_CMD is not set to {FILTER_BIN}."

def test_end_to_end_pipeline():
    # Only test if corpus files are available
    if not os.path.isdir(CLEAN_CORPUS_DIR) or not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.skip("Corpus directories not found, skipping end-to-end test.")

    clean_files = os.listdir(CLEAN_CORPUS_DIR)
    evil_files = os.listdir(EVIL_CORPUS_DIR)

    if clean_files:
        clean_path = os.path.join(CLEAN_CORPUS_DIR, clean_files[0])
        with open(clean_path, 'rb') as f:
            data = f.read()
        req = urllib.request.Request("http://localhost:8080/upload", data=data, method="POST")
        try:
            with urllib.request.urlopen(req) as response:
                assert response.status == 200, f"Clean upload returned status {response.status}, expected 200."
        except urllib.error.HTTPError as e:
            pytest.fail(f"Clean upload failed with HTTP error: {e.code}")

    if evil_files:
        evil_path = os.path.join(EVIL_CORPUS_DIR, evil_files[0])
        with open(evil_path, 'rb') as f:
            data = f.read()
        req = urllib.request.Request("http://localhost:8080/upload", data=data, method="POST")
        try:
            with urllib.request.urlopen(req) as response:
                pytest.fail(f"Evil upload succeeded with status {response.status}, expected 400.")
        except urllib.error.HTTPError as e:
            assert e.code == 400, f"Evil upload returned status {e.code}, expected 400."