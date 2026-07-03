# test_final_state.py

import os
import glob
import yaml
import subprocess
import pytest

def test_config_yaml_fixed():
    config_path = "/home/user/pipeline/config.yaml"
    assert os.path.isfile(config_path), f"Configuration file {config_path} does not exist."

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    assert config is not None, "Config file is empty or invalid YAML."

    assert config.get("redis_port") == 6380, f"redis_port should be 6380, got {config.get('redis_port')}"
    assert config.get("metrics_url") == "http://localhost:9090/report", f"metrics_url should be http://localhost:9090/report, got {config.get('metrics_url')}"

def test_classifier_exists():
    classifier_path = "/home/user/pipeline/classifier.py"
    assert os.path.isfile(classifier_path), f"Classifier script {classifier_path} was not created."

def test_classifier_clean_corpus():
    classifier_path = "/home/user/pipeline/classifier.py"
    clean_files = glob.glob("/app/corpus/clean/*.json")
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["python3", classifier_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected (expected accept/exit code 0). Offending files: {', '.join(failed_files)}"

def test_classifier_evil_corpus():
    classifier_path = "/home/user/pipeline/classifier.py"
    evil_files = glob.glob("/app/corpus/evil/*.json")
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["python3", classifier_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected reject/exit code 1). Offending files: {', '.join(failed_files)}"