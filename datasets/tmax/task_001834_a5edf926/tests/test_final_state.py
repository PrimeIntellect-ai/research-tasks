# test_final_state.py

import os
import glob
import subprocess
import yaml
import pytest

def test_app_config_yaml():
    config_path = "/home/user/app_config.yaml"
    assert os.path.exists(config_path), f"Configuration file {config_path} does not exist."

    with open(config_path, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"Failed to parse {config_path} as YAML: {e}")

    assert isinstance(config, dict), f"{config_path} does not contain a valid YAML dictionary."

    assert config.get("lock_manager_host") == "127.0.0.1", "lock_manager_host is not set to '127.0.0.1'"
    assert config.get("lock_manager_port") == 8001, "lock_manager_port is not set to 8001"
    assert config.get("validator_binary") == "/home/user/validate_queries", "validator_binary is not set to '/home/user/validate_queries'"

def test_validator_binary_exists():
    binary_path = "/home/user/validate_queries"
    assert os.path.exists(binary_path), f"Validator binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Validator binary {binary_path} is not executable."

def test_validator_against_corpora():
    binary_path = "/home/user/validate_queries"
    clean_dir = "/home/user/corpus/clean"
    evil_dir = "/home/user/corpus/evil"

    clean_csvs = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_csvs = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_csvs) > 0, f"No CSV files found in {clean_dir}."
    assert len(evil_csvs) > 0, f"No CSV files found in {evil_dir}."

    failed_clean = []
    for csv_file in clean_csvs:
        result = subprocess.run([binary_path, csv_file], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "ACCEPT":
            failed_clean.append(os.path.basename(csv_file))

    failed_evil = []
    for csv_file in evil_csvs:
        result = subprocess.run([binary_path, csv_file], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "REJECT":
            failed_evil.append(os.path.basename(csv_file))

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_csvs)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_csvs)} evil bypassed/accepted: {', '.join(failed_evil)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))