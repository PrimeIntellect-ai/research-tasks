# test_final_state.py

import os
import json
import subprocess
import tempfile
import urllib.request
import binascii
import struct
import pytest

def test_configs_fixed():
    upload_config_path = "/home/user/config/upload_config.json"
    assert os.path.exists(upload_config_path), f"Missing {upload_config_path}"
    with open(upload_config_path, "r") as f:
        u_conf = json.load(f)
    assert u_conf.get("upload_dir") == "/home/user/uploads/", "upload_config.json does not have the correct upload_dir"

    stats_config_path = "/home/user/config/stats_config.json"
    assert os.path.exists(stats_config_path), f"Missing {stats_config_path}"
    with open(stats_config_path, "r") as f:
        s_conf = json.load(f)
    assert s_conf.get("redis_port") == 6379, "stats_config.json does not have the correct redis_port"

def test_adversarial_corpus():
    binary_path = "/home/user/cbf_filter"
    config_path = "/home/user/config/filter_config.json"
    clean_corpus = "/app/corpus/clean"
    evil_corpus = "/app/corpus/evil"

    assert os.path.exists(binary_path), "cbf_filter binary is missing"
    assert os.access(binary_path, os.X_OK), "cbf_filter is not executable"

    # Test clean corpus
    with tempfile.TemporaryDirectory() as out_dir:
        subprocess.run([binary_path, config_path, clean_corpus, out_dir], check=True)
        clean_files = os.listdir(clean_corpus)
        out_files = os.listdir(out_dir)

        failed_clean = []
        for cf in clean_files:
            if f"{cf}.verified" not in out_files:
                failed_clean.append(cf)

    # Test evil corpus
    with tempfile.TemporaryDirectory() as out_dir:
        subprocess.run([binary_path, config_path, evil_corpus, out_dir], check=True)
        evil_files = os.listdir(evil_corpus)
        out_files = os.listdir(out_dir)

        failed_evil = []
        for ef in evil_files:
            if f"{ef}.verified" in out_files:
                failed_evil.append(ef)

    error_msg = f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {failed_evil}, {len(failed_clean)} of {len(clean_files)} clean modified/dropped: {failed_clean}"
    assert not failed_clean and not failed_evil, error_msg

def create_valid_cbf():
    magic = b"BKUP"
    version = struct.pack("<H", 1)
    flags = struct.pack("<H", 0)
    payload = b"Test Payload Data"
    payload_size = struct.pack("<I", len(payload))
    crc32 = struct.pack("<I", binascii.crc32(payload))
    return magic + version + flags + payload_size + payload + crc32

def test_e2e_flow():
    script_path = "/home/user/process_backups.sh"
    assert os.path.exists(script_path), f"Missing {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

    # Reset Redis state
    subprocess.run(["redis-cli", "del", "verified_backup_count"], check=True)

    # Clear output directory
    verified_dir = "/home/user/verified_backups"
    for f in os.listdir(verified_dir):
        os.remove(os.path.join(verified_dir, f))

    # Place a valid file directly in the uploads directory
    uploads_dir = "/home/user/uploads"
    test_file_path = os.path.join(uploads_dir, "e2e_test.dat")
    with open(test_file_path, "wb") as f:
        f.write(create_valid_cbf())

    # Run the script
    subprocess.run([script_path], check=True)

    # Check if file was processed and renamed
    expected_verified = os.path.join(verified_dir, "e2e_test.dat.verified")
    assert os.path.exists(expected_verified), "process_backups.sh did not produce the verified file"

    # Verify Redis count via stats_api (port 8081)
    try:
        req = urllib.request.Request("http://localhost:8081/")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read().decode('utf-8')
            assert "1" in data or "verified_backup_count" in data, f"Stats API did not return expected count. Got: {data}"
    except Exception as e:
        pytest.fail(f"Failed to query stats_api on port 8081: {e}")