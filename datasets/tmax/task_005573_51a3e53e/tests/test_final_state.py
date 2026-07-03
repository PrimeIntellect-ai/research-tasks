# test_final_state.py

import os
import textwrap
import pytest

def test_operator_env_script():
    env_script = "/home/user/operator_env.sh"
    assert os.path.isfile(env_script), f"File {env_script} does not exist."

    with open(env_script, "r") as f:
        content = f.read().strip().splitlines()

    expected_lines = ["export TZ=UTC", "export LANG=C.UTF-8"]
    assert content == expected_lines, f"Content of {env_script} is incorrect. Expected {expected_lines}, got {content}"

def test_directory_and_symlink():
    manifests_dir = "/home/user/operator/manifests/v1"
    active_symlink = "/home/user/operator/active"

    assert os.path.isdir(manifests_dir), f"Directory {manifests_dir} does not exist."
    assert os.path.islink(active_symlink), f"{active_symlink} is not a symlink."

    target = os.readlink(active_symlink)
    assert target == "/home/user/operator/manifests/v1", f"Symlink {active_symlink} points to {target}, expected /home/user/operator/manifests/v1"

def test_pv_manifests_generated():
    pv_storage = "/home/user/operator/active/pv-storage.yaml"
    pv_db_disk = "/home/user/operator/active/pv-db_disk.yaml"

    assert os.path.isfile(pv_storage), f"Manifest {pv_storage} does not exist."
    assert os.path.isfile(pv_db_disk), f"Manifest {pv_db_disk} does not exist."

    expected_storage = textwrap.dedent("""\
        apiVersion: v1
        kind: PersistentVolume
        metadata:
          name: local-ext4-storage
        spec:
          storageClassName: manual
          local:
            path: /mnt/storage
    """).strip()

    expected_db_disk = textwrap.dedent("""\
        apiVersion: v1
        kind: PersistentVolume
        metadata:
          name: local-ext4-db_disk
        spec:
          storageClassName: manual
          local:
            path: /data/db_disk
    """).strip()

    with open(pv_storage, "r") as f:
        storage_content = f.read().strip()
    assert storage_content == expected_storage, f"Content of {pv_storage} is incorrect."

    with open(pv_db_disk, "r") as f:
        db_disk_content = f.read().strip()
    assert db_disk_content == expected_db_disk, f"Content of {pv_db_disk} is incorrect."

def test_student_script_exists():
    script_path = "/home/user/generate_operator_config.py"
    assert os.path.isfile(script_path), f"Student script {script_path} does not exist."