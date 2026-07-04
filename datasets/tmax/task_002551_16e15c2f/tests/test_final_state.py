# test_final_state.py

import os
import csv
import pytest

def read_csv(path):
    data = {}
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2:
                data[row[0].strip()] = float(row[1].strip())
    return data

def test_dashboard_metrics_mse():
    truth_path = '/tmp/ground_truth_metrics.csv'
    agent_path = '/home/user/dashboard_metrics.csv'

    assert os.path.exists(truth_path), f"Ground truth file missing: {truth_path}"
    assert os.path.exists(agent_path), f"Agent's dashboard_metrics.csv is missing at {agent_path}"

    truth = read_csv(truth_path)
    agent = read_csv(agent_path)

    mse = 0.0
    count = 0
    for ts, true_val in truth.items():
        if ts in agent:
            mse += (agent[ts] - true_val) ** 2
        else:
            mse += (true_val) ** 2 # Heavily penalize missing data
        count += 1

    mse = mse / count if count > 0 else 9999.0

    assert mse <= 0.5, f"MSE of calculated metrics is {mse:.4f}, which exceeds the maximum allowed threshold of 0.5"

def test_logrotate_configuration():
    conf_path = '/home/user/logrotate.conf'
    assert os.path.exists(conf_path), f"Logrotate configuration file missing at {conf_path}"

    with open(conf_path, 'r') as f:
        content = f.read()

    assert '/home/user/raw_telemetry.log' in content, "logrotate.conf does not specify the correct log file: /home/user/raw_telemetry.log"
    assert 'daily' in content, "logrotate.conf is missing the 'daily' rotation directive"
    assert 'rotate 7' in content, "logrotate.conf is missing the 'rotate 7' directive to keep 7 days of backlogs"
    assert 'compress' in content, "logrotate.conf is missing the 'compress' directive"

def test_ssh_permissions_fixed():
    ssh_dir = '/home/user/.ssh'
    auth_keys = '/home/user/.ssh/authorized_keys'

    assert os.path.exists(ssh_dir), f"SSH directory missing: {ssh_dir}"
    assert os.path.exists(auth_keys), f"authorized_keys missing: {auth_keys}"

    dir_stat = os.stat(ssh_dir)
    # Check that group and others have no write permissions on ~/.ssh
    assert (dir_stat.st_mode & 0o022) == 0, f"Permissions on {ssh_dir} are too open (should not be writable by group/others)"

    file_stat = os.stat(auth_keys)
    # Check that group and others have no write permissions on authorized_keys
    assert (file_stat.st_mode & 0o022) == 0, f"Permissions on {auth_keys} are too open (should not be writable by group/others)"