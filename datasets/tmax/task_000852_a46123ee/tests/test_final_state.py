# test_final_state.py

import os

def test_archived_settings_exists_and_redacted():
    archived_path = '/home/user/archived_settings.conf'
    assert os.path.isfile(archived_path), f"The file {archived_path} was not created."

    with open(archived_path, 'r') as f:
        content = f.read()

    expected_lines = [
        "USER=admin",
        "DEBUG=true",
        "LOG_LEVEL=info",
        "SECRET_TOKEN=***",
        "DATABASE_URL=postgres://localhost",
        "SECRET_TOKEN_EXTRA=skip"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' missing or incorrect in {archived_path}."

    assert "super_secret_12345" not in content, "The secret token was not redacted in the archive file."

def test_archive_config_script_exists_and_uses_flock():
    script_path = '/home/user/archive_config.py'
    assert os.path.isfile(script_path), f"The script {script_path} was not created."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "fcntl.flock" in content, "The script does not appear to use 'fcntl.flock'."
    assert "LOCK_SH" in content, "The script does not appear to use 'LOCK_SH' for a shared lock."