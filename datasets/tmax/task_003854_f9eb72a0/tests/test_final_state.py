# test_final_state.py
import os
import subprocess

def test_staging_directory_extracted():
    """Test that the archive was extracted to the staging directory."""
    app_mock_path = "/home/user/staging/bin/app_mock"
    assert os.path.isfile(app_mock_path), f"Extracted file {app_mock_path} is missing."
    assert os.access(app_mock_path, os.X_OK), f"{app_mock_path} should be executable."

def test_app_conf_modified():
    """Test that etc/app.conf was modified correctly."""
    conf_path = "/home/user/staging/etc/app.conf"
    assert os.path.isfile(conf_path), f"Configuration file {conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "listen_port=8080" in content, "listen_port was not updated to 8080 in app.conf."
    assert "db_path=/home/user/staging/data/db.sqlite" in content, "db_path was not updated correctly in app.conf."

def test_manager_script_exists_and_executable():
    """Test that manager.sh exists and is executable."""
    manager_path = "/home/user/manager.sh"
    assert os.path.isfile(manager_path), f"Manager script {manager_path} is missing."
    assert os.access(manager_path, os.X_OK), f"Manager script {manager_path} is not executable."

def test_app_running():
    """Test that the app is running and the PID file exists."""
    pid_file = "/home/user/staging/app.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid numeric PID."

    # Check if process is running
    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} from {pid_file} is not running."

    # Check if the process is actually app_mock
    try:
        with open(f"/proc/{pid}/cmdline", "r") as f:
            cmdline = f.read().replace('\x00', ' ')
        assert "app_mock" in cmdline, f"Process {pid} is not running app_mock. Cmdline: {cmdline}"
    except FileNotFoundError:
        assert False, f"/proc/{pid}/cmdline not found, process might have died."

def test_manager_status_command():
    """Test that manager.sh status exits with 0 when the app is running."""
    manager_path = "/home/user/manager.sh"
    result = subprocess.run([manager_path, "status"], capture_output=True)
    assert result.returncode == 0, f"manager.sh status exited with {result.returncode}, expected 0."

def test_restore_report_log():
    """Test that the restore report log matches the expected format and content."""
    report_path = "/home/user/restore_report.log"
    assert os.path.isfile(report_path), f"Report log {report_path} is missing."

    expected_lines = [
        "[STATUS] RUNNING",
        "[PORT] 8080",
        "[DB] /home/user/staging/data/db.sqlite",
        "[RESULT] RESTORE VALID"
    ]

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in {report_path}."