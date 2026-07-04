# test_final_state.py
import os
import stat
import subprocess
import re

def test_c_file_exists_and_no_hardcoding():
    c_file = "/home/user/verify_restore.c"
    assert os.path.exists(c_file), f"C source file {c_file} is missing."

    with open(c_file, "r") as f:
        content = f.read()

    # Check that the student didn't just hardcode the output
    assert "2525" not in content, "The SMTP port (2525) appears to be hardcoded in the C source."
    assert "FILES: 4" not in content, "The file count (4) appears to be hardcoded in the C source."

def test_c_binary_exists_and_executable():
    binary = "/home/user/verify_restore"
    assert os.path.exists(binary), f"Compiled binary {binary} is missing."
    assert os.access(binary, os.X_OK), f"Binary {binary} is not executable."

def test_bash_script_exists_and_executable():
    script = "/home/user/run_validation.sh"
    assert os.path.exists(script), f"Bash script {script} is missing."
    assert os.access(script, os.X_OK), f"Bash script {script} is not executable."

def test_restore_test_directory_contents():
    restore_dir = "/home/user/restore_test"
    assert os.path.isdir(restore_dir), f"Directory {restore_dir} is missing or not a directory."

    expected_files = {"mail_config.conf", "vm_settings.json", "postfix_main.cf", "aliases"}
    actual_files = set(os.listdir(restore_dir))

    for f in expected_files:
        assert f in actual_files, f"Expected file {f} is missing from {restore_dir}."

    # Check that mail_config.conf contains the expected port
    with open(os.path.join(restore_dir, "mail_config.conf"), "r") as f:
        content = f.read()
        assert "SMTP_PORT=2525" in content, "mail_config.conf does not contain the expected SMTP_PORT."

def test_restore_log_output():
    log_file = "/home/user/restore_log.txt"
    assert os.path.exists(log_file), f"Log file {log_file} is missing. Did you run the bash script?"

    with open(log_file, "r") as f:
        content = f.read().strip()

    expected_output = "RESTORE_CHECK: SUCCESS, FILES: 4, PORT: 2525"
    assert expected_output in content, f"Log file does not contain the expected output. Found: {content}"

def test_c_binary_behavior():
    # Test the binary dynamically to ensure it works properly
    binary = "/home/user/verify_restore"
    restore_dir = "/home/user/restore_test"

    if os.path.exists(binary) and os.path.isdir(restore_dir):
        result = subprocess.run([binary, restore_dir], capture_output=True, text=True)
        assert result.returncode == 0, "C binary did not exit with return code 0."
        expected_output = "RESTORE_CHECK: SUCCESS, FILES: 4, PORT: 2525"
        assert expected_output in result.stdout.strip(), f"C binary output incorrect. Got: {result.stdout}"