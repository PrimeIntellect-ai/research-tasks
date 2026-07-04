# test_final_state.py

import os
import pytest

def test_rotation_status_log():
    status_file = "/home/user/rotation_status.log"
    assert os.path.isfile(status_file), f"File {status_file} is missing."

    with open(status_file, "r") as f:
        content = f.read()

    expected_text = "ROTATED. Previous directory size: 15000 bytes"
    assert expected_text in content, f"Expected '{expected_text}' in {status_file}, but found: {content}"

def test_rotated_log_files():
    app_logs_dir = "/home/user/app_logs"
    app_log = os.path.join(app_logs_dir, "app.log")
    app_log_1 = os.path.join(app_logs_dir, "app.log.1")
    app_log_2 = os.path.join(app_logs_dir, "app.log.2")
    app_log_3 = os.path.join(app_logs_dir, "app.log.3")

    assert os.path.isfile(app_log), f"File {app_log} is missing."
    assert os.path.getsize(app_log) == 0, f"File {app_log} should be exactly 0 bytes (empty)."

    assert os.path.isfile(app_log_1), f"File {app_log_1} is missing."
    assert os.path.getsize(app_log_1) == 12000, f"File {app_log_1} should be exactly 12000 bytes."

    assert os.path.isfile(app_log_2), f"File {app_log_2} is missing."
    assert os.path.getsize(app_log_2) == 2000, f"File {app_log_2} should be exactly 2000 bytes."

    assert os.path.isfile(app_log_3), f"File {app_log_3} is missing."
    assert os.path.getsize(app_log_3) == 1000, f"File {app_log_3} should be exactly 1000 bytes."