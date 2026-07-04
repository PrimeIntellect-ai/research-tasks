# test_final_state.py

import os
import json
import tarfile
import xml.etree.ElementTree as ET

def test_manifest_fixed():
    manifest_path = "/home/user/manifest.xml"
    assert os.path.isfile(manifest_path), f"Fixed manifest {manifest_path} is missing."

    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()
    except ET.ParseError as e:
        assert False, f"Manifest {manifest_path} is not valid XML: {e}"

    parts = root.findall(".//part")
    assert len(parts) > 0, "No <part> elements found in the fixed manifest."
    for part in parts:
        assert "id" in part.attrib, "Missing 'id' attribute in <part> element."
        assert part.text.startswith("backup_part_"), f"Unexpected part text: {part.text}"

def test_assembled_archive():
    archive_path = "/home/user/complete_backup.tar.gz"
    assert os.path.isfile(archive_path), f"Assembled archive {archive_path} is missing."

    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar file."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        assert "logs/system.log" in names, "Archive is missing logs/system.log."
        assert "logs/auth.log" in names, "Archive is missing logs/auth.log."
        assert "/etc/shadow_backup" in names, "Archive is missing the absolute path malicious file."
        assert "../../../root/secret.txt" in names, "Archive is missing the relative path malicious file."

def test_safe_extraction_results():
    system_log = "/home/user/safe_restore/logs/system.log"
    auth_log = "/home/user/safe_restore/logs/auth.log"

    assert os.path.isfile(system_log), f"Safe file {system_log} was not extracted."
    with open(system_log, "r") as f:
        assert f.read() == "system is ok", f"Content of {system_log} is incorrect."

    assert os.path.isfile(auth_log), f"Safe file {auth_log} was not extracted."
    with open(auth_log, "r") as f:
        assert f.read() == "auth fail", f"Content of {auth_log} is incorrect."

def test_malicious_files_not_extracted():
    malicious_abs = "/etc/shadow_backup"
    if os.path.exists(malicious_abs):
        with open(malicious_abs, "r") as f:
            content = f.read()
            assert content != "hacked", f"Malicious absolute path file {malicious_abs} was extracted!"

    # The relative escape path would resolve relative to /home/user/safe_restore
    # /home/user/safe_restore/../../../root/secret.txt -> /root/secret.txt
    malicious_rel = "/root/secret.txt"
    if os.path.exists(malicious_rel):
        with open(malicious_rel, "r") as f:
            content = f.read()
            assert content != "hacked", f"Malicious relative path file {malicious_rel} was extracted!"

def test_quarantine_json():
    quarantine_path = "/home/user/quarantine.json"
    assert os.path.isfile(quarantine_path), f"Quarantine JSON file {quarantine_path} is missing."

    with open(quarantine_path, "r") as f:
        try:
            quarantine_data = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"File {quarantine_path} is not valid JSON: {e}"

    assert isinstance(quarantine_data, list), "Quarantine JSON should be an array."
    assert "/etc/shadow_backup" in quarantine_data, "Missing absolute path in quarantine JSON."
    assert "../../../root/secret.txt" in quarantine_data, "Missing relative path in quarantine JSON."
    assert len(quarantine_data) == 2, "Quarantine JSON should contain exactly 2 malicious paths."

def test_safe_extract_script_exists():
    script_path = "/home/user/safe_extract.py"
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."