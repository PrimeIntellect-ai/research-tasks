# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_executable_exists():
    """Verify that the compiled C program exists."""
    assert os.path.exists("/home/user/setup_spool"), "/home/user/setup_spool does not exist."
    assert os.access("/home/user/setup_spool", os.X_OK), "/home/user/setup_spool is not executable."

def test_idempotency_and_execution():
    """Run the compiled program to test idempotency and ensure it returns 0."""
    result = subprocess.run(["/home/user/setup_spool"], capture_output=True)
    assert result.returncode == 0, f"Execution failed with return code {result.returncode}. Stderr: {result.stderr.decode()}"

def test_directories_and_permissions():
    """Verify directories are created with 0750 permissions."""
    directories = [
        "/home/user/mail_spool",
        "/home/user/mail_spool/inbox",
        "/home/user/mail_spool/outbox",
        "/home/user/mail_spool/archive"
    ]

    for d in directories:
        assert os.path.isdir(d), f"Directory {d} does not exist."
        st = os.stat(d)
        perms = stat.S_IMODE(st.st_mode)
        assert perms == 0o750, f"Directory {d} has incorrect permissions: {oct(perms)}, expected 0o750."

def test_symlink_verification():
    """Verify the tz_local symlink points to the correct timezone file."""
    symlink_path = "/home/user/mail_spool/tz_local"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    target = os.readlink(symlink_path)
    expected_target = "/usr/share/zoneinfo/Europe/Paris"
    assert target == expected_target, f"Symlink points to {target}, expected {expected_target}."

def test_config_file_verification():
    """Verify the mailer.conf file permissions and contents."""
    conf_path = "/home/user/mail_spool/mailer.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} does not exist."

    st = os.stat(conf_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o640, f"File {conf_path} has incorrect permissions: {oct(perms)}, expected 0o640."

    with open(conf_path, "r") as f:
        content = f.read()

    expected_lines = [
        "MAILING_LIST_TZ=Europe/Paris",
        "LC_TIME=fr_FR.UTF-8"
    ]

    lines = content.splitlines()
    assert len(lines) == 2, f"Expected exactly 2 lines in {conf_path}, found {len(lines)}."
    assert lines[0] == expected_lines[0], f"First line is '{lines[0]}', expected '{expected_lines[0]}'."
    assert lines[1] == expected_lines[1], f"Second line is '{lines[1]}', expected '{expected_lines[1]}'."

    # Also verify there's a newline at the end of the last line
    assert content.endswith("\n"), f"{conf_path} does not end with a newline character."