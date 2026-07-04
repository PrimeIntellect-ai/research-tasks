# test_final_state.py

import os
import tarfile
import pytest

def test_sync_configs_script_exists():
    script_path = "/home/user/sync_configs.py"
    assert os.path.isfile(script_path), f"The script {script_path} must exist."

def test_live_config_db_conf_modified():
    db_conf = "/home/user/live_config/db.conf"
    assert os.path.isfile(db_conf), f"{db_conf} must exist."
    with open(db_conf, "r") as f:
        content = f.read()
    expected = "# TRACKED CHANGE\nhost=192.168.1.100\n"
    assert content.strip() == expected.strip(), f"{db_conf} does not have the correct tracked changes."

def test_live_config_new_conf_modified():
    new_conf = "/home/user/live_config/new.conf"
    assert os.path.isfile(new_conf), f"{new_conf} must exist."
    with open(new_conf, "r") as f:
        content = f.read()
    expected = "# TRACKED CHANGE\nmode=fast\n"
    assert content.strip() == expected.strip(), f"{new_conf} does not have the correct tracked changes."

def test_live_config_app_conf_untouched():
    app_conf = "/home/user/live_config/app.conf"
    assert os.path.isfile(app_conf), f"{app_conf} must exist."
    with open(app_conf, "r") as f:
        content = f.read()
    assert content.strip() == "setting=1", f"{app_conf} should not have been modified."

def test_live_config_cache_conf_untouched():
    cache_conf = "/home/user/live_config/cache.conf"
    assert os.path.isfile(cache_conf), f"{cache_conf} must exist."
    with open(cache_conf, "r") as f:
        content = f.read()
    assert content.strip() == "enabled=true", f"{cache_conf} should not have been modified."

def test_tracked_config_archive_exists_and_valid():
    archive_path = "/home/user/tracked_config.tar.gz"
    assert os.path.isfile(archive_path), f"The archive {archive_path} must exist."
    assert tarfile.is_tarfile(archive_path), f"The file {archive_path} must be a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        # Get basenames of files in the archive to account for different archiving methods
        names = [os.path.basename(m.name) for m in tar.getmembers() if m.isfile()]

        for expected_file in ["app.conf", "db.conf", "cache.conf", "new.conf"]:
            assert expected_file in names, f"{expected_file} must be in the new tracked archive."

        # Optional: check content of one of the files in the archive
        db_member = next((m for m in tar.getmembers() if os.path.basename(m.name) == "db.conf"), None)
        assert db_member is not None, "db.conf must be found in the archive."

        f = tar.extractfile(db_member)
        content = f.read().decode('utf-8')
        assert "# TRACKED CHANGE" in content, "The archived db.conf must contain the tracked change header."