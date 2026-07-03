# test_final_state.py

import os
import stat
import subprocess
import pytest

CONFIG_DIR = "/home/user/config_vault"
CONFIG_FILE = "/home/user/config_vault/app_config.json"
CHECK_PERMS_C = "/home/user/check_perms.c"
CHECK_PERMS_EXE = "/home/user/check_perms"
VERIFY_SCRIPT = "/home/user/verify.sh"
STATUS_FILE = "/home/user/security_status.txt"

def test_config_file_content():
    assert os.path.exists(CONFIG_FILE), f"File {CONFIG_FILE} does not exist"
    with open(CONFIG_FILE, "r") as f:
        content = f.read()
    assert content == '{"status":"locked"}', f"Incorrect content in {CONFIG_FILE}"

def test_permissions():
    assert os.path.exists(CONFIG_DIR), f"Directory {CONFIG_DIR} does not exist"
    dir_stat = os.stat(CONFIG_DIR)
    assert stat.S_IMODE(dir_stat.st_mode) == 0o700, f"Incorrect permissions for {CONFIG_DIR}"

    assert os.path.exists(CONFIG_FILE), f"File {CONFIG_FILE} does not exist"
    file_stat = os.stat(CONFIG_FILE)
    assert stat.S_IMODE(file_stat.st_mode) == 0o400, f"Incorrect permissions for {CONFIG_FILE}"

def test_security_status_file():
    assert os.path.exists(STATUS_FILE), f"File {STATUS_FILE} does not exist"
    with open(STATUS_FILE, "r") as f:
        content = f.read()
    assert content == "SECURE\n", f"Incorrect content in {STATUS_FILE}"

def test_check_perms_executable():
    assert os.path.exists(CHECK_PERMS_EXE), f"Executable {CHECK_PERMS_EXE} does not exist"
    assert os.access(CHECK_PERMS_EXE, os.X_OK), f"{CHECK_PERMS_EXE} is not executable"

    # Test correct state
    os.chmod(CONFIG_DIR, 0o700)
    os.chmod(CONFIG_FILE, 0o400)
    result = subprocess.run([CHECK_PERMS_EXE], capture_output=True, text=True)
    assert result.stdout == "SECURE\n", f"Expected SECURE\\n, got {result.stdout!r}"

    # Test incorrect file permission
    os.chmod(CONFIG_FILE, 0o600)
    result = subprocess.run([CHECK_PERMS_EXE], capture_output=True, text=True)
    assert result.stdout == "INSECURE\n", f"Expected INSECURE\\n, got {result.stdout!r}"

    # Test incorrect dir permission
    os.chmod(CONFIG_FILE, 0o400)
    os.chmod(CONFIG_DIR, 0o755)
    result = subprocess.run([CHECK_PERMS_EXE], capture_output=True, text=True)
    assert result.stdout == "INSECURE\n", f"Expected INSECURE\\n, got {result.stdout!r}"

    # Restore correct state
    os.chmod(CONFIG_DIR, 0o700)

def test_verify_script():
    assert os.path.exists(VERIFY_SCRIPT), f"Script {VERIFY_SCRIPT} does not exist"
    assert os.access(VERIFY_SCRIPT, os.X_OK), f"{VERIFY_SCRIPT} is not executable"
    with open(VERIFY_SCRIPT, "r") as f:
        content = f.read()
    assert "TZ=UTC" in content, f"TZ=UTC not found in {VERIFY_SCRIPT}"
    assert "LC_ALL=C" in content, f"LC_ALL=C not found in {VERIFY_SCRIPT}"