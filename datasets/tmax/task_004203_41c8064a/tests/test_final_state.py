# test_final_state.py

import os
import json
import hashlib

def test_script_exists():
    script_path = '/home/user/process_assets.py'
    assert os.path.exists(script_path), f"Expected script at {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} should be a file."

def test_extracted_directories_exist():
    base_dir = '/home/user/extracted'
    assert os.path.isdir(base_dir), f"Expected directory {base_dir} is missing."

    assert os.path.isdir(os.path.join(base_dir, 'module1')), "module1 directory missing."
    assert os.path.isdir(os.path.join(base_dir, 'module2')), "module2 directory missing."

def test_zip_files_deleted():
    base_dir = '/home/user/extracted'
    assert not os.path.exists(os.path.join(base_dir, 'module1.zip')), "module1.zip was not deleted."
    assert not os.path.exists(os.path.join(base_dir, 'module2.zip')), "module2.zip was not deleted."

def test_log_files_modified():
    app_log_path = '/home/user/extracted/module1/app.log'
    db_log_path = '/home/user/extracted/module2/db.log'

    assert os.path.isfile(app_log_path), f"{app_log_path} is missing."
    with open(app_log_path, 'r') as f:
        app_log_content = f.read()

    assert "DEBUG" not in app_log_content, "DEBUG lines were not removed from app.log."
    assert "WARN:" not in app_log_content, "WARN was not replaced in app.log."
    assert "WARNING: high memory usage detected" in app_log_content, "WARNING replacement incorrect in app.log."

    assert os.path.isfile(db_log_path), f"{db_log_path} is missing."
    with open(db_log_path, 'r') as f:
        db_log_content = f.read()

    assert "DEBUG" not in db_log_content, "DEBUG lines were not removed from db.log."
    assert "WARN:" not in db_log_content, "WARN was not replaced in db.log."
    assert "WARNING: reconnecting to database" in db_log_content, "WARNING replacement incorrect in db.log."

def test_manifest_exists_and_tmp_does_not():
    manifest_path = '/home/user/final_manifest.json'
    tmp_path = '/home/user/final_manifest.json.tmp'

    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."
    assert not os.path.exists(tmp_path), f"Temporary manifest file {tmp_path} should have been renamed/deleted."

def test_manifest_content():
    manifest_path = '/home/user/final_manifest.json'
    base_dir = '/home/user/extracted'

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            assert False, "Manifest is not a valid JSON file."

    expected_files = {
        'module1/app.log',
        'module1/main.py',
        'module2/db.log',
        'module2/config.yml'
    }

    assert set(manifest.keys()) == expected_files, f"Manifest keys do not match expected files. Found: {list(manifest.keys())}"

    for rel_path, expected_hash in manifest.items():
        abs_path = os.path.join(base_dir, rel_path)
        assert os.path.isfile(abs_path), f"File {abs_path} listed in manifest does not exist."

        with open(abs_path, 'rb') as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()

        assert actual_hash == expected_hash, f"Hash mismatch for {rel_path}. Expected {expected_hash}, got {actual_hash}."