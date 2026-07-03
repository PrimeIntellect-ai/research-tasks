# test_final_state.py

import os
import stat
import subprocess
import json
import pytest

EXPORTER_C_PATH = "/home/user/exporter.c"
EXPORTER_BIN_PATH = "/home/user/exporter"
SCRIPT_PATH = "/home/user/collect_and_rotate.sh"
DB_PATH = "/home/user/app_data/db.sqlite"
METRICS_LOG_PATH = "/home/user/metrics.log"
BACKUP_LOG_PATH = "/home/user/backups/metrics_backup.log"

def get_expected_iface():
    with open("/proc/net/route", "r") as f:
        lines = f.readlines()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) > 1 and parts[1] == "00000000":
            return parts[0]
    return None

def test_exporter_c_exists():
    assert os.path.isfile(EXPORTER_C_PATH), f"Source file {EXPORTER_C_PATH} is missing."

def test_exporter_bin_exists_and_executable():
    assert os.path.isfile(EXPORTER_BIN_PATH), f"Executable {EXPORTER_BIN_PATH} is missing."
    st = os.stat(EXPORTER_BIN_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"{EXPORTER_BIN_PATH} is not executable."

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"{SCRIPT_PATH} is not executable."

def test_exporter_output():
    expected_iface = get_expected_iface()
    assert expected_iface is not None, "Could not determine default interface from /proc/net/route"
    expected_size = os.path.getsize(DB_PATH)

    result = subprocess.run([EXPORTER_BIN_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {EXPORTER_BIN_PATH} failed."

    output = result.stdout.strip()
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        pytest.fail(f"Output of {EXPORTER_BIN_PATH} is not valid JSON: {output}")

    assert "default_iface" in data, "Output JSON missing 'default_iface' key."
    assert "db_size" in data, "Output JSON missing 'db_size' key."
    assert data["default_iface"] == expected_iface, f"Expected default_iface '{expected_iface}', got '{data['default_iface']}'"
    assert data["db_size"] == expected_size, f"Expected db_size {expected_size}, got {data['db_size']}"

def test_backup_log_contains_metrics():
    assert os.path.isfile(BACKUP_LOG_PATH), f"Backup log {BACKUP_LOG_PATH} is missing."

    expected_iface = get_expected_iface()
    expected_size = os.path.getsize(DB_PATH)

    with open(BACKUP_LOG_PATH, "r") as f:
        content = f.read()

    # We check if the expected JSON is in the backup log
    # It might have been appended or written directly. We just check if a valid line exists.
    found = False
    for line in content.strip().split('\n'):
        if not line:
            continue
        try:
            data = json.loads(line)
            if data.get("default_iface") == expected_iface and data.get("db_size") == expected_size:
                found = True
                break
        except json.JSONDecodeError:
            pass

    assert found, f"Backup log {BACKUP_LOG_PATH} does not contain the expected JSON metrics."

def test_metrics_log_is_truncated():
    assert os.path.isfile(METRICS_LOG_PATH), f"Metrics log {METRICS_LOG_PATH} is missing."
    size = os.path.getsize(METRICS_LOG_PATH)
    assert size == 0, f"Metrics log {METRICS_LOG_PATH} should be 0 bytes (truncated), but is {size} bytes."