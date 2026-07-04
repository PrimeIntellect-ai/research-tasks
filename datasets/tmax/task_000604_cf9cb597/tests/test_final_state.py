# test_final_state.py

import os
import tarfile
import stat
import pytest

def test_operator_script_exists_and_executable():
    script_path = "/home/user/operator.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"Script {script_path} is not executable."

def test_backup_archive_created():
    backup_path = "/home/user/backups/manifest_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup archive {backup_path} does not exist."

    with tarfile.open(backup_path, "r:gz") as tar:
        names = tar.getnames()
        # The tarball might include the directory name or just the files.
        # We check if any path ends with old-config.yaml
        assert any(name.endswith("old-config.yaml") for name in names), "Backup archive does not contain 'old-config.yaml'."

def test_manifests_synced():
    active_dir = "/home/user/active_manifests"
    incoming_dir = "/home/user/incoming_manifests"

    for filename in ["pv-data.yaml", "svc-web.yaml", "svc-api.yaml"]:
        assert os.path.isfile(os.path.join(active_dir, filename)), f"File {filename} was not synced to {active_dir}."

def test_mock_fstab_generated():
    fstab_path = "/home/user/mock_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_line = "/home/user/raw_data /mnt/data/db-volume none bind 0 0"
    assert expected_line in content, f"Expected line '{expected_line}' not found in {fstab_path}."

def test_fw_rules_generated():
    fw_rules_path = "/home/user/fw_rules.sh"
    assert os.path.isfile(fw_rules_path), f"File {fw_rules_path} does not exist."

    with open(fw_rules_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_rules = [
        "iptables -A INPUT -p tcp --dport 30080 -j ACCEPT",
        "iptables -A INPUT -p tcp --dport 30443 -j ACCEPT"
    ]

    for rule in expected_rules:
        assert rule in content, f"Expected rule '{rule}' not found in {fw_rules_path}."