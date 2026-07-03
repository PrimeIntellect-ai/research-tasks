# test_final_state.py
import os
import tarfile
import pytest

def test_config_backup_exists_and_valid():
    backup_path = "/home/user/backups/config_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} is missing."

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            # The tarball is of /home/user/config, so it could contain 'config/app.conf', 'home/user/config/app.conf', or 'app.conf'
            assert any(name.endswith("app.conf") for name in names), "app.conf not found in the backup tarball."
    except tarfile.ReadError:
        pytest.fail(f"Backup file {backup_path} is not a valid gzip-compressed tarball.")

def test_app_conf_fixed():
    conf_path = "/home/user/config/app.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "upstream_socket=/home/user/run/aggregator.sock" in content, "The upstream_socket path was not correctly fixed in app.conf."

def test_supervisor_script_fixed():
    script_path = "/home/user/supervisor.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "sleep 5" in content, "The supervisor.sh script does not contain 'sleep 5'."

def test_dashboard_metrics():
    metrics_path = "/home/user/dashboard_metrics.txt"
    assert os.path.isfile(metrics_path), f"Metrics file {metrics_path} is missing."

    expected_lines = [
        "[2023-10-25 14:01] - 3 errors",
        "[2023-10-25 14:02] - 2 errors",
        "[2023-10-25 14:04] - 1 errors"
    ]

    with open(metrics_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Dashboard metrics do not match expected output. Got: {actual_lines}"