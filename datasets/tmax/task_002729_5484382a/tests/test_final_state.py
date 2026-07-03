# test_final_state.py

import os
import pytest

def test_bsdiff4_installed():
    try:
        import bsdiff4
    except ImportError:
        pytest.fail("bsdiff4 is not installed or cannot be imported. The package installation failed.")

def test_setup_fixed():
    setup_py_path = "/app/bsdiff4-1.2.4/setup.py"
    assert os.path.isfile(setup_py_path), f"setup.py missing at {setup_py_path}"
    with open(setup_py_path, "r") as f:
        content = f.read()
    assert "core_broken.c" not in content, "The deliberate misconfiguration 'core_broken.c' is still present in setup.py"
    assert "core.c" in content, "The setup.py does not contain the fixed 'core.c' source file reference."

def test_backup_script_exists():
    script_path = "/home/user/backup.py"
    assert os.path.isfile(script_path), f"Backup script missing at {script_path}"
    with open(script_path, "r") as f:
        content = f.read()
    assert "fcntl" in content, "The backup script does not seem to import or use fcntl for file locking."
    assert "LOCK_SH" in content, "The backup script does not seem to use fcntl.LOCK_SH for shared locks."

def test_patch_files_exist():
    backup_dir = "/home/user/backup_dir"
    expected_patches = ["data.bin.patch", "logs.txt.patch"]
    for patch in expected_patches:
        patch_path = os.path.join(backup_dir, patch)
        assert os.path.isfile(patch_path), f"Expected patch file {patch} is missing in {backup_dir}"

def test_patch_size_metric():
    backup_dir = '/home/user/backup_dir'
    assert os.path.isdir(backup_dir), f"Backup directory missing at {backup_dir}"

    patch_files = [f for f in os.listdir(backup_dir) if f.endswith('.patch')]
    assert len(patch_files) > 0, "No .patch files found in backup directory."

    patch_size = sum(os.path.getsize(os.path.join(backup_dir, f)) for f in patch_files)

    assert patch_size > 0, "Total patch size is 0 bytes. Expected > 0."
    assert patch_size <= 50000, f"Total patch size {patch_size} bytes exceeds the storage efficiency threshold of 50000 bytes."

def test_base_files_intact():
    backup_dir = "/home/user/backup_dir"
    data_bin = os.path.join(backup_dir, "data.bin")
    logs_txt = os.path.join(backup_dir, "logs.txt")

    assert os.path.isfile(data_bin), f"Base file {data_bin} is missing."
    assert os.path.isfile(logs_txt), f"Base file {logs_txt} is missing."

    assert os.path.getsize(data_bin) == 1000000, f"{data_bin} size changed. It should be left intact."
    assert os.path.getsize(logs_txt) == 500000, f"{logs_txt} size changed. It should be left intact."