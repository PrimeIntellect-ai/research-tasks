# test_final_state.py

import os
import json
import subprocess
import pytest

CONFIG_PATH = "/home/user/config.json"
FILTER_SCRIPT = "/home/user/dataset_filter.py"
CLEAN_CORPUS = "/app/corpora/clean"
EVIL_CORPUS = "/app/corpora/evil"

def test_config_generated_correctly():
    assert os.path.isfile(CONFIG_PATH), f"Missing generated configuration file: {CONFIG_PATH}"

    with open(CONFIG_PATH, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Configuration file {CONFIG_PATH} is not valid JSON.")

    assert "max_depth" in config, "Missing 'max_depth' in config.json"
    assert "max_files" in config, "Missing 'max_files' in config.json"

    assert config["max_depth"] == 5, f"Expected max_depth to be 5, got {config['max_depth']}"
    assert config["max_files"] == 42, f"Expected max_files to be 42, got {config['max_files']}"

def test_filter_script_exists():
    assert os.path.isfile(FILTER_SCRIPT), f"Missing filter script: {FILTER_SCRIPT}"

def test_filter_script_behavior():
    assert os.path.isfile(FILTER_SCRIPT), f"Filter script missing, cannot test behavior."

    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]

    clean_failed = []
    evil_failed = []

    for c_file in clean_files:
        result = subprocess.run(["python3", FILTER_SCRIPT, c_file], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(c_file))

    for e_file in evil_files:
        result = subprocess.run(["python3", FILTER_SCRIPT, e_file], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(e_file))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))