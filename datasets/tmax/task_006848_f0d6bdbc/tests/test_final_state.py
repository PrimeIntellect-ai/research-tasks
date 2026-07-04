# test_final_state.py

import json
import os
import tarfile
import pytest

def test_deploy_monitor_exists():
    path = '/home/user/deploy_monitor.py'
    assert os.path.exists(path), f"File {path} does not exist. The deploy_monitor.py script is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_backup_exists_and_valid():
    backup_path = '/home/user/backups/auth_backup.tar.gz'
    assert os.path.exists(backup_path), f"Backup file {backup_path} does not exist. The monitor may not have detected the crash or created the backup."
    assert os.path.isfile(backup_path), f"Path {backup_path} is not a file."
    assert tarfile.is_tarfile(backup_path), f"Backup file {backup_path} is not a valid tar archive."

def test_deployment_report_exists_and_valid():
    report_path = '/home/user/deployment_report.json'
    assert os.path.exists(report_path), f"Deployment report {report_path} does not exist."
    assert os.path.isfile(report_path), f"Path {report_path} is not a file."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert report.get('auth_restarted') is True, "The 'auth_restarted' field in the report must be true."

    backups = report.get('backups_created', [])
    assert isinstance(backups, list), "'backups_created' must be a list."
    assert 'auth_backup.tar.gz' in backups, "'auth_backup.tar.gz' must be in the 'backups_created' list."

    pids = report.get('active_pids', {})
    assert isinstance(pids, dict), "'active_pids' must be a dictionary."
    for svc in ['auth', 'data', 'web']:
        assert svc in pids, f"Service '{svc}' is missing from 'active_pids'."
        assert isinstance(pids[svc], int), f"PID for '{svc}' must be an integer."

def test_running_processes_and_environment():
    report_path = '/home/user/deployment_report.json'
    if not os.path.exists(report_path):
        pytest.fail(f"Cannot verify processes because {report_path} is missing.")

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Cannot verify processes because report is invalid JSON.")

    pids = report.get('active_pids', {})
    if not isinstance(pids, dict) or not all(k in pids for k in ['auth', 'data', 'web']):
        pytest.fail("Cannot verify processes because 'active_pids' structure is invalid.")

    for svc, pid in pids.items():
        env_file = f"/proc/{pid}/environ"
        assert os.path.exists(env_file), f"Process {pid} for service '{svc}' is not running."

        try:
            with open(env_file, 'rb') as f:
                env_data = f.read().split(b'\0')
        except Exception as e:
            pytest.fail(f"Could not read environment for PID {pid} (service '{svc}'): {e}")

        env_dict = {}
        for item in env_data:
            if b'=' in item:
                k, v = item.split(b'=', 1)
                env_dict[k.decode('utf-8', errors='ignore')] = v.decode('utf-8', errors='ignore')

        assert env_dict.get('TZ') == 'UTC', f"Service '{svc}' (PID {pid}) does not have TZ=UTC in its environment."
        assert env_dict.get('LC_ALL') == 'C.UTF-8', f"Service '{svc}' (PID {pid}) does not have LC_ALL=C.UTF-8 in its environment."