# test_final_state.py

import os
import subprocess
import tarfile

def test_backup_img_exists_and_ext4():
    img_path = '/home/user/backup.img'
    assert os.path.isfile(img_path), f"File {img_path} does not exist"

    # Check size
    size = os.path.getsize(img_path)
    assert size == 20971520, f"Expected {img_path} size to be 20971520 bytes, got {size}"

    # Check ext4 format
    try:
        output = subprocess.check_output(['file', img_path], text=True)
        assert 'ext4' in output.lower(), f"Expected {img_path} to be formatted as ext4, got: {output}"
    except subprocess.CalledProcessError:
        pytest.fail(f"Failed to run 'file' command on {img_path}")

def test_system_fstab_configured():
    fstab_path = '/home/user/system_fstab'
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist"

    with open(fstab_path, 'r') as f:
        lines = f.readlines()

    found = False
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 6:
            if parts[0] == '/home/user/backup.img' and parts[1] == '/home/user/mnt_backup' and parts[2] == 'ext4':
                if parts[3] == 'loop,defaults' and parts[4] == '0' and parts[5] == '2':
                    found = True
                    break

    assert found, "The fstab entry for /home/user/backup.img is missing or incorrect in /home/user/system_fstab"

def test_run_provision_script():
    script_path = '/home/user/run_provision.py'
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist"

    with open(script_path, 'r') as f:
        content = f.read()

    assert 'pexpect' in content, f"The script {script_path} does not seem to import or use 'pexpect'"

def test_tarball_created():
    tarball_path = '/home/user/app_data_backup.tar.gz'
    assert os.path.isfile(tarball_path), f"Tarball {tarball_path} was not created"

    assert tarfile.is_tarfile(tarball_path), f"File {tarball_path} is not a valid tar archive"

    try:
        with tarfile.open(tarball_path, 'r:gz') as tar:
            names = tar.getnames()
            assert 'config.json' in names or './config.json' in names, "Expected config.json in tarball"
            assert 'data.bin' in names or './data.bin' in names, "Expected data.bin in tarball"
    except tarfile.ReadError:
        assert False, f"File {tarball_path} is not a valid gzip compressed tar archive"

def test_provision_summary_log():
    log_path = '/home/user/provision_summary.log'
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist"

    with open(log_path, 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) == 3, f"Expected exactly 3 lines in {log_path}, got {len(content)}"

    assert content[0] == 'FSTAB_CONFIGURED=true', f"Line 1 incorrect: {content[0]}"
    assert content[1] == 'BACKUP_ARCHIVE_CREATED=true', f"Line 2 incorrect: {content[1]}"
    assert content[2] == 'BACKUP_IMG_SIZE=20971520', f"Line 3 incorrect: {content[2]}"