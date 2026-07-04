# test_final_state.py
import os
import pytest

def test_archived_logs_exists_and_content():
    archive_path = '/home/user/archived_logs.bak'
    assert os.path.exists(archive_path), f"Archive file {archive_path} not found."

    with open(archive_path, 'r') as f:
        archive_contents = f.read()

    expected_snippets = [
        "--- /home/user/data/logs/app1/db.log ---\nerror at line 1\nerror at line 2\n",
        "--- /home/user/data/logs/app2/auth.log ---\nlogin success user admin\nlogin failed user test\n",
        "--- /home/user/data/logs/app2/nested/build.log ---\ncompilation finished\n"
    ]

    for snippet in expected_snippets:
        assert snippet in archive_contents, f"Missing or incorrectly formatted snippet in archive:\n{snippet}"

    assert "server.log" not in archive_contents, "Active log server.log was incorrectly archived."
    assert "metrics.log" not in archive_contents, "Active log metrics.log was incorrectly archived."

def test_inactive_logs_truncated():
    inactive_logs = [
        '/home/user/data/logs/app1/db.log',
        '/home/user/data/logs/app2/auth.log',
        '/home/user/data/logs/app2/nested/build.log'
    ]
    for log in inactive_logs:
        assert os.path.exists(log), f"Log file {log} was deleted instead of truncated."
        assert os.path.getsize(log) == 0, f"Inactive log file {log} was not truncated to 0 bytes."

def test_active_logs_unmodified():
    active_logs = {
        "/home/user/data/logs/app1/server.log": "writing active data...\n",
        "/home/user/data/logs/app2/nested/metrics.log": "metric stream\n"
    }
    for filepath, expected_content in active_logs.items():
        assert os.path.exists(filepath), f"Active log file {filepath} is missing."
        assert os.path.getsize(filepath) > 0, f"Active log file {filepath} was incorrectly truncated."
        with open(filepath, "r") as f:
            content = f.read()
        assert content == expected_content, f"Content of active log {filepath} was modified."

def test_script_uses_fcntl():
    script_path = '/home/user/reclaimer.py'
    assert os.path.exists(script_path), f"Script {script_path} not found."
    with open(script_path, 'r') as f:
        code = f.read()
    assert 'fcntl.flock' in code or 'fcntl' in code, f"The script {script_path} does not use fcntl for locking."