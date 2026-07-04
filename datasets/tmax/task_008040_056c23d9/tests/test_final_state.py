# test_final_state.py
import os
import re
import gzip
import pytest

def test_go_script_exists():
    assert os.path.isfile("/home/user/vm_monitor.go"), "The Go script /home/user/vm_monitor.go does not exist."

def test_logrotate_conf_exists_and_configured():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"The logrotate config {conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "daily" in content, "logrotate.conf must specify 'daily' rotation."
    assert "rotate 3" in content, "logrotate.conf must specify 'rotate 3'."
    assert "compress" in content, "logrotate.conf must specify 'compress'."
    assert "create" in content, "logrotate.conf must specify 'create'."

def test_active_log_file_contents():
    log_path = "/home/user/migration_storage.log"
    assert os.path.isfile(log_path), f"The active log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 1, f"Expected exactly 1 line in active log, found {len(lines)}."

    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] TOTAL_VIRTUAL_BYTES=59055800320 EXCEEDS_QUOTA=true$"
    assert re.match(pattern, lines[0]), f"Active log line does not match expected format: {lines[0]}"

def test_rotated_log_file_contents():
    rotated_log_path = "/home/user/migration_storage.log.1.gz"
    assert os.path.isfile(rotated_log_path), f"The rotated log file {rotated_log_path} does not exist."

    with gzip.open(rotated_log_path, "rt") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 1, f"Expected exactly 1 line in rotated log, found {len(lines)}."

    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] TOTAL_VIRTUAL_BYTES=59055800320 EXCEEDS_QUOTA=true$"
    assert re.match(pattern, lines[0]), f"Rotated log line does not match expected format: {lines[0]}"