# test_final_state.py

import os
import stat

def test_edge_fstab_exists_and_content():
    fstab_path = '/home/user/edge_fstab'
    assert os.path.exists(fstab_path), f"File {fstab_path} does not exist."
    with open(fstab_path, 'r') as f:
        content = f.read().strip()
    expected_line = "UUID=EDGE_SENSOR_DRIVE /home/user/sensor_mnt ext4 defaults,noatime 0 2"
    assert expected_line in content, f"File {fstab_path} does not contain the expected mount configuration."

def test_sensor_logger_exists():
    logger_path = '/home/user/sensor_logger.py'
    assert os.path.exists(logger_path), f"File {logger_path} does not exist."
    assert os.path.isfile(logger_path), f"{logger_path} is not a regular file."

def test_deploy_script_exists_and_executable():
    deploy_path = '/home/user/deploy.sh'
    assert os.path.exists(deploy_path), f"File {deploy_path} does not exist."
    assert os.path.isfile(deploy_path), f"{deploy_path} is not a regular file."
    assert os.access(deploy_path, os.X_OK), f"File {deploy_path} is not executable."

def test_telemetry_log_exists_and_content():
    telemetry_path = '/home/user/sensor_mnt/telemetry.log'
    assert os.path.exists(telemetry_path), f"File {telemetry_path} does not exist. Did the Python script run?"
    with open(telemetry_path, 'r') as f:
        content = f.read().strip()
    assert content == "EDGE_DATA_ACTIVE", f"Expected 'EDGE_DATA_ACTIVE' in {telemetry_path}, got '{content}'."

def test_deploy_status_log_exists_and_content():
    status_path = '/home/user/deploy_status.log'
    assert os.path.exists(status_path), f"File {status_path} does not exist. Did deploy.sh execute?"
    with open(status_path, 'r') as f:
        content = f.read().strip()
    assert content == "DEPLOYMENT_SUCCESS", f"Expected 'DEPLOYMENT_SUCCESS' in {status_path}, got '{content}'."