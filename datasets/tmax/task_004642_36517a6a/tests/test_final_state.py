# test_final_state.py

import os
import stat
import tarfile
import pytest

def test_manifests_permissions():
    path = "/home/user/manifests"
    assert os.path.exists(path), f"Directory {path} does not exist."
    st = os.stat(path)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o700, f"Permissions for {path} are {oct(mode)}, expected 0o700."

def test_certs_exist_and_non_empty():
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.getsize(cert_path) > 0, f"Certificate file {cert_path} is empty."

    assert os.path.isfile(key_path), f"Key file {key_path} does not exist."
    assert os.path.getsize(key_path) > 0, f"Key file {key_path} is empty."

def test_backup_tarball_valid():
    backup_path = "/home/user/backups/manifests.tar.gz"
    assert os.path.isfile(backup_path), f"Backup archive {backup_path} does not exist."

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            # The paths inside the tar may vary, but the file names must be present
            basenames = [os.path.basename(name) for name in names]
            assert "deployment.yaml" in basenames, "deployment.yaml not found in backup archive."
            assert "service.yaml" in basenames, "service.yaml not found in backup archive."
    except tarfile.ReadError:
        pytest.fail(f"Backup archive {backup_path} is not a valid gzip-compressed tarball.")

def test_status_log_content():
    log_path = "/home/user/status.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected = "Backup successful: manifests.tar.gz"
    assert content == expected, f"Log file content is '{content}', expected '{expected}'."