# test_final_state.py

import os

def test_app_logs_directory_exists():
    """Verify that the required log directory was created."""
    dir_path = "/home/user/app/logs"
    assert os.path.isdir(dir_path), f"Expected directory {dir_path} does not exist."

def test_daemon_executable_exists():
    """Verify that the Go application was compiled to the expected binary."""
    daemon_path = "/home/user/app/daemon"
    assert os.path.isfile(daemon_path), f"Expected executable {daemon_path} does not exist."
    assert os.access(daemon_path, os.X_OK), f"The file {daemon_path} is not executable."

def test_app_log_file_exists():
    """Verify that the daemon successfully ran and created its log file."""
    log_file_path = "/home/user/app/logs/app.log"
    assert os.path.isfile(log_file_path), f"Expected log file {log_file_path} does not exist. Did the daemon run successfully?"

def test_success_txt_contents():
    """Verify that the success.txt file contains the correct daemon startup message."""
    success_file_path = "/home/user/success.txt"
    assert os.path.isfile(success_file_path), f"Expected output file {success_file_path} does not exist."

    with open(success_file_path, "r") as f:
        content = f.read().strip()

    expected_message = "Daemon initialized: Log rotation configured for /home/user/app/logs/app.log"
    assert expected_message in content, f"The file {success_file_path} does not contain the expected success message. Found: {content}"

def test_main_go_modified():
    """Verify that main.go was correctly modified in-place."""
    main_go_path = "/home/user/app/main.go"
    assert os.path.isfile(main_go_path), f"Expected source file {main_go_path} does not exist."

    with open(main_go_path, "r") as f:
        content = f.read()

    assert "/var/log/customdaemon/app.log" not in content, "The old restricted path was not removed from main.go."
    assert "/home/user/app/logs/app.log" in content, "The new local path was not found in main.go."