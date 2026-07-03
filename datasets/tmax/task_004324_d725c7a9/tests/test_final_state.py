# test_final_state.py

import os
import json
import pytest

APP_DIR = "/home/user/app"
EXT_DIR = os.path.join(APP_DIR, "ext")
LOG_FILE = "/home/user/migration_result.log"

def test_validator_c_updated_for_python3():
    filepath = os.path.join(EXT_DIR, "validator.c")
    assert os.path.isfile(filepath), f"File missing: {filepath}"

    with open(filepath, "r") as f:
        content = f.read()

    assert "Py_InitModule" not in content, "validator.c still contains Python 2 'Py_InitModule'."
    assert "PyModuleDef" in content, "validator.c does not contain 'PyModuleDef' for Python 3."
    assert "PyModule_Create" in content, "validator.c does not contain 'PyModule_Create' for Python 3."

def test_makefile_updated_for_python3():
    filepath = os.path.join(EXT_DIR, "Makefile")
    assert os.path.isfile(filepath), f"File missing: {filepath}"

    with open(filepath, "r") as f:
        content = f.read()

    assert "python3.10" in content, "Makefile does not include Python 3.10 headers."
    assert "python2.7" not in content, "Makefile still includes Python 2.7 headers."

def test_validator_so_copied():
    filepath = os.path.join(APP_DIR, "validator.so")
    assert os.path.isfile(filepath), f"Compiled extension missing at: {filepath}"

def test_config_py_created_and_has_rate_limit():
    filepath = os.path.join(APP_DIR, "config.py")
    assert os.path.isfile(filepath), f"config.py missing: {filepath}"

    with open(filepath, "r") as f:
        content = f.read()

    assert "RATE_LIMIT" in content, "config.py does not contain RATE_LIMIT."

def test_server_py_updated():
    filepath = os.path.join(APP_DIR, "server.py")
    assert os.path.isfile(filepath), f"File missing: {filepath}"

    with open(filepath, "r") as f:
        content = f.read()

    assert "RATE_LIMIT = 100" not in content, "server.py still defines RATE_LIMIT."
    assert "config" in content, "server.py does not import from config."

def test_auth_py_updated():
    filepath = os.path.join(APP_DIR, "auth.py")
    assert os.path.isfile(filepath), f"File missing: {filepath}"

    with open(filepath, "r") as f:
        content = f.read()

    assert "from server import RATE_LIMIT" not in content, "auth.py still imports RATE_LIMIT from server."
    assert "config" in content, "auth.py does not import from config."

def test_migration_result_log_success():
    assert os.path.isfile(LOG_FILE), f"Migration result log missing: {LOG_FILE}. Did you run test_runner.py?"

    with open(LOG_FILE, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail("migration_result.log does not contain valid JSON.")

    assert data.get("status") == "ok", f"Expected status 'ok', got: {data.get('status')}"