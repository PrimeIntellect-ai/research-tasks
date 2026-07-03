# test_final_state.py

import os
import zipfile
import ast

def test_script_exists():
    script_path = "/home/user/atomic_update.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_script_uses_required_modules():
    script_path = "/home/user/atomic_update.py"
    with open(script_path, "r") as f:
        content = f.read()

    assert "fcntl" in content, "Script does not import or use fcntl for file locking."
    assert "tempfile" in content, "Script does not use tempfile for atomic writes."
    assert "os.replace" in content or "replace" in content, "Script does not use os.replace for atomic replacement."

def test_lockfile_exists():
    lock_path = "/home/user/master_config.zip.lock"
    assert os.path.isfile(lock_path), f"Lockfile {lock_path} was not created."

def test_zip_archive_updated_correctly():
    zip_path = "/home/user/master_config.zip"
    assert os.path.isfile(zip_path), f"Archive {zip_path} does not exist."
    assert zipfile.is_zipfile(zip_path), f"Archive {zip_path} is not a valid zip file."

    with zipfile.ZipFile(zip_path, 'r') as z:
        files = z.namelist()

        assert "db.json" in files, "db.json missing from updated archive."
        assert "cache.json" in files, "cache.json missing from updated archive."
        assert "web.json" in files, "web.json missing from updated archive."

        with z.open("db.json") as f:
            db_content = f.read().decode('utf-8').strip()
            assert db_content == '{"db_host": "new.local", "port": 5432}', "db.json was not properly updated from incoming configs."

        with z.open("cache.json") as f:
            cache_content = f.read().decode('utf-8').strip()
            assert cache_content == '{"cache_size": 1024}', "cache.json was not properly added from incoming configs."

        with z.open("web.json") as f:
            web_content = f.read().decode('utf-8').strip()
            assert web_content == '{"workers": 4}', "web.json was incorrectly modified or removed."