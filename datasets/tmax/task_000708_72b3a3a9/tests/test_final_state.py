# test_final_state.py

import os
import tarfile
import pytest

def test_patch_log_contents():
    log_path = "/home/user/patch_log.txt"
    assert os.path.isfile(log_path), f"Missing patch log file at {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = ["app.conf", "web.conf"]
    assert lines == expected_lines, f"Expected {log_path} to contain {expected_lines}, but got {lines}"

def test_patch_archive_contents():
    archive_path = "/home/user/configs_patch.tar.bz2"
    assert os.path.isfile(archive_path), f"Missing patch archive at {archive_path}"

    try:
        with tarfile.open(archive_path, "r:bz2") as tar:
            members = tar.getnames()
    except tarfile.TarError as e:
        pytest.fail(f"Failed to read {archive_path} as a bzip2 tarball: {e}")

    expected_members = {"app.conf", "web.conf"}
    assert set(members) == expected_members, f"Archive {archive_path} should contain exactly {expected_members}, but contains {members}"

def test_modified_files():
    current_configs_dir = "/home/user/configs_current"

    # Check web.conf
    web_conf_path = os.path.join(current_configs_dir, "web.conf")
    assert os.path.isfile(web_conf_path), f"Missing {web_conf_path}"
    with open(web_conf_path, "r") as f:
        web_content = f.read()
    assert "LOG_LEVEL=debug" in web_content, f"web.conf missing LOG_LEVEL=debug replacement"
    assert "SERVER_PORT=9000" in web_content, f"web.conf missing SERVER_PORT=9000 replacement"
    assert "DEBUG_LEVEL=1" not in web_content, f"web.conf still contains DEBUG_LEVEL=1"
    assert "SERVER_PORT=8080" not in web_content, f"web.conf still contains SERVER_PORT=8080"
    assert "WORKERS=8" in web_content, f"web.conf missing WORKERS=8"

    # Check app.conf
    app_conf_path = os.path.join(current_configs_dir, "app.conf")
    assert os.path.isfile(app_conf_path), f"Missing {app_conf_path}"
    with open(app_conf_path, "r") as f:
        app_content = f.read()
    assert "LOG_LEVEL=debug" in app_content, f"app.conf missing LOG_LEVEL=debug replacement"
    assert "SERVER_PORT=9000" in app_content, f"app.conf missing SERVER_PORT=9000 replacement"
    assert "DEBUG_LEVEL=1" not in app_content, f"app.conf still contains DEBUG_LEVEL=1"
    assert "SERVER_PORT=8080" not in app_content, f"app.conf still contains SERVER_PORT=8080"
    assert "MODULES=auth,payment,shipping" in app_content, f"app.conf missing MODULES=auth,payment,shipping"

def test_unmodified_files():
    current_configs_dir = "/home/user/configs_current"

    # Check db.conf
    db_conf_path = os.path.join(current_configs_dir, "db.conf")
    assert os.path.isfile(db_conf_path), f"Missing {db_conf_path}"
    with open(db_conf_path, "r") as f:
        db_content = f.read()
    assert "DEBUG_LEVEL=0" in db_content, "db.conf should not be modified"
    assert "SERVER_PORT=5432" in db_content, "db.conf should not be modified"

    # Check cache.conf
    cache_conf_path = os.path.join(current_configs_dir, "cache.conf")
    assert os.path.isfile(cache_conf_path), f"Missing {cache_conf_path}"
    with open(cache_conf_path, "r") as f:
        cache_content = f.read()
    assert "DEBUG_LEVEL=0" in cache_content, "cache.conf should not be modified"
    assert "SERVER_PORT=6379" in cache_content, "cache.conf should not be modified"