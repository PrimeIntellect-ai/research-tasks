# test_final_state.py

import os
import re
import pytest

def test_init_db_auto_exp_exists_and_executable():
    path = "/home/user/migration_project/init_db_auto.exp"
    assert os.path.isfile(path), f"Expect script {path} does not exist."
    assert os.access(path, os.X_OK), f"Expect script {path} is not executable."

    with open(path, "r") as f:
        content = f.read()
        assert "migrate123" in content, f"{path} does not contain the required password 'migrate123'."

def test_env_setup_sh_exists_and_exports():
    path = "/home/user/migration_project/env_setup.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."

    with open(path, "r") as f:
        content = f.read()
        assert "DATA_PATH" in content, f"{path} does not set DATA_PATH."
        assert "/home/user/migration_project/data" in content, f"{path} does not set the correct DATA_PATH value."

def test_deploy_sh_exists_and_executable():
    path = "/home/user/migration_project/deploy.sh"
    assert os.path.isfile(path), f"Deployment script {path} does not exist."
    assert os.access(path, os.X_OK), f"Deployment script {path} is not executable."

    with open(path, "r") as f:
        content = f.read()
        assert "env_setup.sh" in content, f"{path} does not source env_setup.sh."
        assert "cargo build --release" in content, f"{path} does not compile the Rust app."
        assert "init_db_auto.exp" in content, f"{path} does not execute init_db_auto.exp."
        assert "wait" in content, f"{path} does not use 'wait' to wait for background processes."

def test_rust_main_rs_modified():
    path = "/home/user/migration_project/rust_app/src/main.rs"
    assert os.path.isfile(path), f"Rust source {path} does not exist."

    with open(path, "r") as f:
        content = f.read()
        assert "sleep" in content, f"{path} does not use sleep for retrying."
        assert "Connection established" in content, f"{path} does not contain the success message."

def test_app_log_contains_success_message():
    path = "/home/user/migration_project/app.log"
    assert os.path.isfile(path), f"Log file {path} does not exist. Did you run deploy.sh?"

    with open(path, "r") as f:
        content = f.read()
        assert "Connection established" in content, f"{path} does not contain 'Connection established'."