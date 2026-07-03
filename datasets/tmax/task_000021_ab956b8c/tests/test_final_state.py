# test_final_state.py

import os
import glob

LOG_FILE = "/home/user/operator.log"
BACKUP_DIR = "/home/user/backups"

def test_waiting_for_network():
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    with open(LOG_FILE, "r") as f:
        log_contents = f.read()

    wait_count = log_contents.count("WAITING FOR NETWORK")
    assert wait_count >= 1, "Expected 'WAITING FOR NETWORK' to appear in operator.log while waiting for routing.ready."

def test_manifest_backup():
    assert os.path.isdir(BACKUP_DIR), f"Backup directory {BACKUP_DIR} does not exist."
    backups = glob.glob(os.path.join(BACKUP_DIR, "app.conf.*.bak"))
    assert len(backups) == 1, f"Expected exactly 1 backup file for app.conf, found {len(backups)}."

def test_qemu_network_string():
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    with open(LOG_FILE, "r") as f:
        log_contents = f.read()

    expected_qemu_cmd = "RUNNING QEMU: -m 256 -name backend -netdev user,id=net0,hostfwd=tcp:127.0.0.1:9090-:3000 -device e1000,netdev=net0"
    assert expected_qemu_cmd in log_contents, f"Expected QEMU command not found in {LOG_FILE}. Make sure the constructed command exactly matches the requirements."

def test_restart_policy():
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    with open(LOG_FILE, "r") as f:
        log_contents = f.read()

    restart_count = log_contents.count("RESTARTING backend")
    assert restart_count == 2, f"Expected exactly 2 'RESTARTING backend' messages in {LOG_FILE}, found {restart_count}. The mock fails twice and succeeds on the third try."