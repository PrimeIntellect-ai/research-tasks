# test_final_state.py

import os
import stat

def test_directories_exist():
    """Verify that required directories exist."""
    assert os.path.isdir("/home/user/service_data"), "Directory /home/user/service_data is missing."
    assert os.path.isdir("/home/user/backup"), "Directory /home/user/backup is missing."

def test_backup_file_correct():
    """Verify the backup file was created and contains the initial state."""
    backup_path = "/home/user/backup/passwd.bak"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} is missing."

    with open(backup_path, "r") as f:
        content = f.read()

    assert "dummyuser:x:1000:1000:Dummy:/home/dummy:/bin/bash" in content, "Backup file does not contain the original dummyuser entry."

def test_passwd_file_correct():
    """Verify the mock passwd file contains the correct entries and is idempotent."""
    passwd_path = "/home/user/service_data/passwd"
    assert os.path.isfile(passwd_path), f"File {passwd_path} is missing."

    with open(passwd_path, "r") as f:
        lines = f.readlines()

    appuser_lines = [line.strip() for line in lines if line.startswith("appuser:")]
    assert len(appuser_lines) == 1, f"Expected exactly one 'appuser' entry, found {len(appuser_lines)}. Script may not be idempotent."

    expected_appuser = "appuser:x:2001:2001:Microservice Account:/home/user/service_data:/bin/false"
    assert appuser_lines[0] == expected_appuser, f"The appuser entry does not match the expected string. Got: {appuser_lines[0]}"

    dummy_present = any("dummyuser:x:1000:1000:Dummy:/home/dummy:/bin/bash" in line for line in lines)
    assert dummy_present, "The original dummyuser entry was removed or modified in the passwd file."

def test_verify_script_exists_and_robust():
    """Verify the generated Python script exists and contains error handling."""
    script_path = "/home/user/service_data/verify.py"
    assert os.path.isfile(script_path), f"Python verification script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "Error: passwd file missing" in content, "The Python script does not contain the exact required error message string 'Error: passwd file missing'."
    assert "try:" in content or "try " in content, "The Python script does not appear to use a try-except block for error handling."

def test_result_log_correct():
    """Verify the result log contains the correct output."""
    log_path = "/home/user/result.log"
    assert os.path.isfile(log_path), f"Result log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert content == "UID: 2001\n", f"Result log content is incorrect. Expected 'UID: 2001\\n', got {repr(content)}"

def test_init_script_executable():
    """Verify the init script exists and is executable."""
    script_path = "/home/user/init_service.sh"
    assert os.path.isfile(script_path), f"Deployment script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deployment script {script_path} is not executable."