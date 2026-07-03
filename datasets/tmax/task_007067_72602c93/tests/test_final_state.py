# test_final_state.py

import os
import glob
import tarfile
import tempfile
import subprocess
import pytest

def test_merged_archive_exists():
    assert os.path.isfile("/home/user/update.tar.gz"), "Merged archive /home/user/update.tar.gz is missing"

def test_extracted_configs_exist():
    assert os.path.isfile("/home/user/extracted/configs/app1.conf"), "app1.conf missing in extracted directory"
    assert os.path.isfile("/home/user/extracted/configs/app2.conf"), "app2.conf missing in extracted directory"

def test_zip_slip_prevented():
    # Verify malicious files were not extracted
    assert not os.path.exists("/home/user/extracted/malicious/escape.txt"), "Malicious escape file was extracted!"
    assert not os.path.exists("/tmp/setup_configs/malicious/absolute.txt"), "Malicious absolute file was extracted!"
    assert not os.path.exists("/home/user/extracted/../malicious/escape.txt"), "Malicious escape file was extracted outside target!"

def test_config_modifications():
    for app in ["app1.conf", "app2.conf"]:
        path = f"/home/user/extracted/configs/{app}"
        with open(path, "r") as f:
            lines = f.read().splitlines()

        assert len(lines) > 0, f"{app} is empty"

        # Check LOG_LEVEL
        log_levels = [line for line in lines if line.startswith("LOG_LEVEL=")]
        assert len(log_levels) == 1, f"Expected exactly one LOG_LEVEL in {app}"
        assert log_levels[0] == "LOG_LEVEL=TRACE", f"LOG_LEVEL not set to TRACE in {app}"

        # Check MANAGED_BY
        assert lines[-1] == "MANAGED_BY=SECURE_CONF_MANAGER", f"Last line of {app} is not MANAGED_BY=SECURE_CONF_MANAGER"

def test_safe_update_archive_exists():
    assert os.path.isfile("/home/user/safe_update.tar.gz"), "Repackaged archive /home/user/safe_update.tar.gz is missing"

def test_split_chunks_exist_and_valid():
    chunks = sorted(glob.glob("/home/user/outgoing/safe_update.tar.gz.chunk-*"))
    assert len(chunks) > 0, "No chunks found in /home/user/outgoing/"

    # Check chunk size (all but last should be 500 bytes)
    for chunk in chunks[:-1]:
        assert os.path.getsize(chunk) == 500, f"Chunk {chunk} is not exactly 500 bytes"

    # Concatenate chunks and verify tarball
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        for chunk in chunks:
            with open(chunk, "rb") as f:
                tmp.write(f.read())
        tmp_path = tmp.name

    try:
        assert tarfile.is_tarfile(tmp_path), "Concatenated chunks do not form a valid tar archive"
        with tarfile.open(tmp_path, "r:gz") as tar:
            names = tar.getnames()
            assert any(name.endswith("app1.conf") for name in names), "app1.conf not found in the repackaged archive"
            assert any(name.endswith("app2.conf") for name in names), "app2.conf not found in the repackaged archive"
    finally:
        os.remove(tmp_path)