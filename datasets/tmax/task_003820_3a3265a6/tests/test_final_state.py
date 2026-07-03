# test_final_state.py
import os
import base64
import tarfile
import tempfile
import shutil
import pytest

def test_script_exists():
    script_path = "/home/user/safe_archive.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    # It should ideally be executable, but at least it must exist.
    # We will check if it exists and is a file.

def test_archive_log_contents():
    log_path = "/home/user/archive_log.txt"
    assert os.path.exists(log_path), f"Log file missing: {log_path}"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "config.yml",
        "ext_link.conf",
        "huge_routing.conf.part_aa",
        "huge_routing.conf.part_ab",
        "huge_routing.conf.part_ac",
        "settings.json"
    ]
    assert lines == expected, f"Log file contents do not match exactly. Expected {expected}, got {lines}"

def test_backup_archive_contents():
    backup_path = "/home/user/config_backup.tar.gz.b64"
    assert os.path.exists(backup_path), f"Backup file missing: {backup_path}"

    temp_dir = tempfile.mkdtemp()
    try:
        # Decode base64
        b64_decoded_path = os.path.join(temp_dir, "backup.tar.gz")
        with open(backup_path, 'rb') as f_in, open(b64_decoded_path, 'wb') as f_out:
            try:
                base64.decode(f_in, f_out)
            except Exception as e:
                pytest.fail(f"Failed to decode base64 from {backup_path}: {e}")

        # Open tar.gz
        try:
            with tarfile.open(b64_decoded_path, "r:gz") as tar:
                tar.extractall(path=temp_dir)
        except tarfile.TarError as e:
            pytest.fail(f"Failed to open or extract tar.gz file: {e}")

        # Collect extracted files, ignoring the tar archive itself
        extracted_files = []
        for root, dirs, files in os.walk(temp_dir):
            if root == temp_dir and "backup.tar.gz" in files:
                files.remove("backup.tar.gz")
            for f in files:
                extracted_files.append(f)

        expected = {
            "config.yml",
            "ext_link.conf",
            "huge_routing.conf.part_aa",
            "huge_routing.conf.part_ab",
            "huge_routing.conf.part_ac",
            "settings.json"
        }

        assert set(extracted_files) == expected, f"Extracted files do not match expected set. Expected {expected}, got {set(extracted_files)}"

        # Verify chunks match original file
        orig_large_file = "/home/user/app_configs/app3/huge_routing.conf"
        with open(orig_large_file, 'rb') as f:
            orig_data = f.read()

        # Find extracted chunks
        chunk_aa = None
        chunk_ab = None
        chunk_ac = None

        for root, dirs, files in os.walk(temp_dir):
            if "huge_routing.conf.part_aa" in files:
                chunk_aa = os.path.join(root, "huge_routing.conf.part_aa")
            if "huge_routing.conf.part_ab" in files:
                chunk_ab = os.path.join(root, "huge_routing.conf.part_ab")
            if "huge_routing.conf.part_ac" in files:
                chunk_ac = os.path.join(root, "huge_routing.conf.part_ac")

        assert chunk_aa and chunk_ab and chunk_ac, "One or more huge_routing.conf chunks are missing from the extracted archive."

        with open(chunk_aa, 'rb') as f: data_aa = f.read()
        with open(chunk_ab, 'rb') as f: data_ab = f.read()
        with open(chunk_ac, 'rb') as f: data_ac = f.read()

        assert len(data_aa) == 1048576, f"part_aa size is {len(data_aa)}, expected 1048576 (1MB)"
        assert len(data_ab) == 1048576, f"part_ab size is {len(data_ab)}, expected 1048576 (1MB)"

        reconstructed = data_aa + data_ab + data_ac
        assert reconstructed == orig_data, "Reconstructed huge_routing.conf does not match the original file data."

        # Verify small files
        for fname, orig_path in [
            ("config.yml", "/home/user/app_configs/app1/config.yml"),
            ("settings.json", "/home/user/app_configs/app2/settings.json"),
            ("ext_link.conf", "/home/user/external_configs/ext.conf")
        ]:
            extracted_path = None
            for root, dirs, files in os.walk(temp_dir):
                if fname in files:
                    extracted_path = os.path.join(root, fname)
                    break
            assert extracted_path, f"File {fname} not found in extracted archive."
            with open(orig_path, 'rb') as f_orig, open(extracted_path, 'rb') as f_ext:
                assert f_orig.read() == f_ext.read(), f"Contents of {fname} do not match the original."

    finally:
        shutil.rmtree(temp_dir)