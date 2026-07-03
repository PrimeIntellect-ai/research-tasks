# test_final_state.py

import os
import re
import pytest

STAGED_CONFIGS_DIR = "/home/user/staged_configs"
STORE_DIR = "/home/user/store"
DEPLOY_DIR = "/home/user/deploy"
LOG_FILE = "/home/user/deployment_report.log"
RUST_PROJECT_DIR = "/home/user/config_deployer"

def test_staged_configs_exist_and_transformed():
    assert os.path.exists(STAGED_CONFIGS_DIR), f"Directory {STAGED_CONFIGS_DIR} does not exist."
    assert os.path.isdir(STAGED_CONFIGS_DIR), f"{STAGED_CONFIGS_DIR} is not a directory."

    for i in range(1, 21):
        filename = f"config_{i:02d}.ini"
        filepath = os.path.join(STAGED_CONFIGS_DIR, filename)
        assert os.path.exists(filepath), f"File {filepath} does not exist."
        assert os.path.isfile(filepath), f"{filepath} is not a file."

        with open(filepath, 'r') as f:
            content = f.read()

        assert "HOST=127.0.0.1" in content, f"'HOST=127.0.0.1' missing in {filepath}"
        assert "LOG_LEVEL=debug" in content, f"'LOG_LEVEL=debug' missing in {filepath}"
        assert "HOST=localhost" not in content, f"'HOST=localhost' still present in {filepath}"
        assert "DEBUG=true" not in content, f"'DEBUG=true' still present in {filepath}"

def test_rust_project_exists():
    assert os.path.exists(RUST_PROJECT_DIR), f"Rust project directory {RUST_PROJECT_DIR} does not exist."
    cargo_toml = os.path.join(RUST_PROJECT_DIR, "Cargo.toml")
    assert os.path.exists(cargo_toml), f"Cargo.toml missing in {RUST_PROJECT_DIR}."

def test_deploy_and_store_directories_exist():
    assert os.path.exists(STORE_DIR), f"Directory {STORE_DIR} does not exist."
    assert os.path.isdir(STORE_DIR), f"{STORE_DIR} is not a directory."
    assert os.path.exists(DEPLOY_DIR), f"Directory {DEPLOY_DIR} does not exist."
    assert os.path.isdir(DEPLOY_DIR), f"{DEPLOY_DIR} is not a directory."

def test_hard_links_and_store_files():
    for i in range(1, 21):
        basename = f"config_{i:02d}.ini"
        staged_path = os.path.join(STAGED_CONFIGS_DIR, basename)
        deploy_path = os.path.join(DEPLOY_DIR, basename)

        assert os.path.exists(deploy_path), f"Deployed file {deploy_path} does not exist."

        size = os.path.getsize(staged_path)
        store_filename = f"config_{i:02d}_{size}.ini"
        store_path = os.path.join(STORE_DIR, store_filename)

        assert os.path.exists(store_path), f"Stored file {store_path} does not exist."

        deploy_stat = os.stat(deploy_path)
        store_stat = os.stat(store_path)

        assert deploy_stat.st_ino == store_stat.st_ino, f"{deploy_path} and {store_path} are not hard links (different inodes)."

def test_deployment_report_log():
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} does not exist."

    with open(LOG_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 20, f"Expected 20 lines in {LOG_FILE}, found {len(lines)}."

    pattern = re.compile(r"^LINKED config_\d{2}\.ini -> store/config_\d{2}_\d+\.ini$")
    for line in lines:
        assert pattern.match(line), f"Log line format incorrect: '{line}'"