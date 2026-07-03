# test_final_state.py

import os
import pytest

OUTBOX_DIR = "/home/user/project_outbox"
SECURITY_LOG = "/home/user/security.log"
SCRIPT_PATH = "/home/user/unpack.py"

def test_script_exists_and_uses_mmap():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} is missing."
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert "mmap" in content, "The script must use the 'mmap' module as per requirements."

def test_valid_files_extracted_with_correct_encoding():
    # File 1: docs/info.txt
    info_txt_path = os.path.join(OUTBOX_DIR, "docs/info.txt")
    assert os.path.isfile(info_txt_path), f"Valid file {info_txt_path} was not extracted."

    with open(info_txt_path, "rb") as f:
        content_bytes = f.read()

    try:
        content_str = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail(f"File {info_txt_path} is not valid UTF-8.")

    assert content_str == "Project start: © 2023", f"Content of {info_txt_path} does not match expected UTF-8 output."

    # File 2: src/main.py
    main_py_path = os.path.join(OUTBOX_DIR, "src/main.py")
    assert os.path.isfile(main_py_path), f"Valid file {main_py_path} was not extracted."

    with open(main_py_path, "rb") as f:
        content_bytes = f.read()

    try:
        content_str = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail(f"File {main_py_path} is not valid UTF-8.")

    assert content_str == "print('Hello äöü')", f"Content of {main_py_path} does not match expected UTF-8 output."

def test_zip_slip_prevention():
    # Ensure malicious paths were not resolved and written outside the outbox
    ssh_key_path = "/home/user/.ssh/authorized_keys"
    config_path = "/home/user/config.json"

    assert not os.path.exists(ssh_key_path), f"Zip-slip vulnerability triggered! File written to {ssh_key_path}"
    assert not os.path.exists(config_path), f"Zip-slip vulnerability triggered! File written to {config_path}"

    # Also ensure they weren't written inside the outbox with literal ".." names if resolved incorrectly
    # Though standard resolution usually handles this, we mainly check the security log.

def test_security_log_contents():
    assert os.path.isfile(SECURITY_LOG), f"Security log {SECURITY_LOG} was not created."

    with open(SECURITY_LOG, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_malicious_paths = [
        "../../.ssh/authorized_keys",
        "../config.json"
    ]

    for path in expected_malicious_paths:
        assert path in lines, f"Malicious path '{path}' was not logged in {SECURITY_LOG}."