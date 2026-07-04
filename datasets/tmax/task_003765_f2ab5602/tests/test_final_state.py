# test_final_state.py

import os
import json
import pytest

def test_quarantine_invalid_file():
    quarantine_path = "/home/user/quarantine/config_25.json"
    assert os.path.isfile(quarantine_path), f"Expected invalid file to be moved to {quarantine_path}"

def test_reconstructed_configs_exist():
    expected_files = [
        "config_10.json",
        "config_20.json",
        "config_30.json",
        "config_40.json",
        "config_50.json"
    ]
    for f in expected_files:
        filepath = os.path.join("/home/user/reconstructed_configs", f)
        assert os.path.isfile(filepath), f"Reconstructed file {filepath} is missing."

def test_imputation_logic():
    # Helper to read json
    def read_json(filename):
        with open(os.path.join("/home/user/reconstructed_configs", filename), "r") as f:
            return json.load(f)

    config_10 = read_json("config_10.json")
    config_20 = read_json("config_20.json")
    config_30 = read_json("config_30.json")
    config_40 = read_json("config_40.json")
    config_50 = read_json("config_50.json")

    # config_20.json
    # max_memory should be linearly interpolated: at 10=1024, at 30=3072. at 20 -> 2048
    assert config_20["max_memory"] == 2048, "config_20.json max_memory should be 2048 (linear interpolation)"
    assert isinstance(config_20["max_memory"], int), "max_memory must be an integer"
    # log_level should be forward-filled from 10 ("INFO")
    assert config_20["log_level"] == "INFO", "config_20.json log_level should be 'INFO' (forward-fill)"

    # config_30.json
    # timeout should be linearly interpolated: at 20=2.0, at 40=4.0. at 30 -> 3.0
    assert config_30["timeout"] == 3.0, "config_30.json timeout should be 3.0 (linear interpolation)"
    assert isinstance(config_30["timeout"], float), "timeout must be a float"

    # config_40.json
    # log_level should be forward-filled from 30 ("DEBUG")
    assert config_40["log_level"] == "DEBUG", "config_40.json log_level should be 'DEBUG' (forward-fill)"

def test_pipeline_logs():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        log_content = f.read()

    expected_logs = [
        "[STAGE: VALIDATION] Quarantined 1 invalid files.",
        "[STAGE: IMPUTATION] Imputed 4 missing values across all files.",
        "[STAGE: LOAD] Successfully wrote 5 reconstructed configs."
    ]

    for expected in expected_logs:
        assert expected in log_content, f"Expected log string '{expected}' not found in {log_path}"