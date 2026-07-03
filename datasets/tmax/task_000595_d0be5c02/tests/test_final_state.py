# test_final_state.py

import os
import re
import tarfile
import pytest

BASE_DIR = "/home/user/k8s-operator"

def test_operator_script_exists():
    script_path = os.path.join(BASE_DIR, "operator.py")
    assert os.path.isfile(script_path), f"Operator script missing: {script_path}"

def test_backup_created():
    backups_dir = os.path.join(BASE_DIR, "backups")
    files = os.listdir(backups_dir)
    tar_files = [f for f in files if f.endswith('.tar.gz')]

    assert len(tar_files) == 1, f"Expected exactly 1 tar.gz file in backups, found {len(tar_files)}"
    backup_file = tar_files[0]

    match = re.match(r"^backup_\d{8}_\d{6}\.tar\.gz$", backup_file)
    assert match, f"Backup filename {backup_file} does not match required format."

    backup_path = os.path.join(backups_dir, backup_file)
    with tarfile.open(backup_path, "r:gz") as tar:
        members = tar.getnames()
        # The file should be at the root of the archive, possibly prefixed with './'
        assert "app.yaml" in members or "./app.yaml" in members, "Backup does not contain app.yaml at the root level."

        member_name = "app.yaml" if "app.yaml" in members else "./app.yaml"
        f = tar.extractfile(member_name)
        assert f is not None, "Could not extract app.yaml from backup."

        content = f.read().decode('utf-8')
        assert "replicas: 1" in content, "Backup app.yaml does not contain 'replicas: 1' (it should be the original file)."
        assert "operator.k8s.io/processed-at" not in content, "Backup app.yaml should not contain the processed-at annotation."

def test_active_manifests_updated():
    active_dir = os.path.join(BASE_DIR, "active")
    app_yaml = os.path.join(active_dir, "app.yaml")
    service_yaml = os.path.join(active_dir, "service.yaml")

    assert os.path.isfile(app_yaml), f"Active app.yaml missing: {app_yaml}"
    assert os.path.isfile(service_yaml), f"Active service.yaml missing: {service_yaml}"

    # The timezone annotation should be present and formatted correctly
    annotation_pattern = re.compile(r'operator\.k8s\.io/processed-at:\s*"?\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \+0900"?')

    with open(app_yaml, "r") as f:
        app_content = f.read()
    assert "replicas: 3" in app_content, "Active app.yaml does not have 'replicas: 3' from incoming."
    assert annotation_pattern.search(app_content), "Active app.yaml missing correctly formatted processed-at annotation."

    with open(service_yaml, "r") as f:
        service_content = f.read()
    assert annotation_pattern.search(service_content), "Active service.yaml missing correctly formatted processed-at annotation."

def test_incoming_empty():
    incoming_dir = os.path.join(BASE_DIR, "incoming")
    files = os.listdir(incoming_dir)
    assert len(files) == 0, f"Incoming directory is not empty: {files}"

def test_operator_log():
    log_file = os.path.join(BASE_DIR, "operator.log")
    assert os.path.isfile(log_file), f"Log file missing: {log_file}"

    with open(log_file, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) >= 1, "Log file is empty."
    last_line = lines[-1]

    log_pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \+0900\] SUCCESS: Backed up to backup_\d{8}_\d{6}\.tar\.gz and processed 2 manifests\.$")
    assert log_pattern.match(last_line), f"Log line does not match required format: {last_line}"