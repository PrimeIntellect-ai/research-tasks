# test_final_state.py

import os
import json
import tarfile
import pytest
import re

def test_config_xml_redacted():
    config_path = "/home/user/data_to_backup/config.xml"
    assert os.path.isfile(config_path), f"File missing: {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    # Original IPs should not be present
    original_ips = ["192.168.1.100", "10.0.0.5", "172.16.0.1", "172.16.0.2"]
    for ip in original_ips:
        assert ip not in content, f"Sensitive IP {ip} was not redacted in config.xml"

    # Verify replacement string exists
    assert "XXX.XXX.XXX.XXX" in content, "The exact replacement string 'XXX.XXX.XXX.XXX' was not found in config.xml"

    # Verify no other IPv4-like strings remain, optionally (but let's just check the replacement count)
    redacted_count = content.count("XXX.XXX.XXX.XXX")
    assert redacted_count >= 4, f"Expected at least 4 redactions, found {redacted_count}"

def test_extracted_errors_json():
    json_path = "/home/user/extracted_errors.json"
    assert os.path.isfile(json_path), f"File missing: {json_path}"

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{json_path} is not valid JSON")

    assert isinstance(data, list), "JSON root should be a list"
    assert len(data) == 2, f"Expected 2 error objects, found {len(data)}"

    # Object 1
    err1 = data[0]
    assert err1.get("timestamp") == "2023-10-01 10:15:30", "Incorrect timestamp for first error"
    assert err1.get("level") == "ERROR", "Incorrect level for first error"
    assert err1.get("message") == "NullPointerException in processing module", "Incorrect message for first error"
    assert "at com.app.Module.process" in err1.get("traceback", ""), "Missing traceback content in first error"

    # Object 2
    err2 = data[1]
    assert err2.get("timestamp") == "2023-10-01 10:16:05", "Incorrect timestamp for second error"
    assert err2.get("level") == "ERROR", "Incorrect level for second error"
    assert err2.get("message") == "Database connection failed", "Incorrect message for second error"
    assert "at com.db.Connection.connect" in err2.get("traceback", ""), "Missing traceback content in second error"
    assert "Caused by: TimeoutException" in err2.get("traceback", ""), "Missing caused-by in second error traceback"

def test_backup_tar_gz():
    tar_path = "/home/user/backup.tar.gz"
    assert os.path.isfile(tar_path), f"Archive missing: {tar_path}"
    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar archive"

    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getnames()

    # Must contain config.xml and app.log
    # Note: they might be stored as './config.xml' or 'config.xml' depending on how relpath worked
    # We'll check if any member ends with the filename
    def contains_file(filename):
        return any(m == filename or m.endswith("/" + filename) for m in members)

    assert contains_file("config.xml"), "config.xml is missing from the backup archive"
    assert contains_file("app.log"), "app.log is missing from the backup archive"

    # Must NOT contain symlinks
    forbidden_links = ["to_b", "to_a", "docs_link"]
    for m in members:
        for link in forbidden_links:
            assert not m.endswith(link), f"Symlink {link} was improperly included in the backup archive"

    # Verify that the config.xml inside the tarball is the redacted one
    with tarfile.open(tar_path, "r:gz") as tar:
        config_member = next((m for m in tar.getmembers() if m.name.endswith("config.xml")), None)
        assert config_member is not None, "Could not find config.xml member to read"

        f = tar.extractfile(config_member)
        content = f.read().decode("utf-8")
        assert "192.168.1.100" not in content, "config.xml inside the tarball still contains sensitive IPs"
        assert "XXX.XXX.XXX.XXX" in content, "config.xml inside the tarball is not redacted correctly"