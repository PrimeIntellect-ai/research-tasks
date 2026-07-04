# test_final_state.py

import os
import tarfile
import stat

def test_script_exists_and_executable():
    script_path = "/home/user/rebuild_env.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script is not executable: {script_path}"

def test_active_directory_state():
    active_dir = "/home/user/app_data/active"
    assert os.path.isdir(active_dir), f"Directory missing: {active_dir}"

    items = set(os.listdir(active_dir))
    expected_items = {"db.conf", "keys.json"}

    # Check for stale links/files removal
    stale_items = items - expected_items
    assert not stale_items, f"Stale files/links not removed from active directory: {stale_items}"

    # Check for required items
    missing_items = expected_items - items
    assert not missing_items, f"Required files/links missing from active directory: {missing_items}"

    # Verify db.conf symlink
    db_conf_path = os.path.join(active_dir, "db.conf")
    assert os.path.islink(db_conf_path), f"{db_conf_path} is not a symlink"
    db_target = os.readlink(db_conf_path)
    # The target might be absolute or relative, but usually absolute based on instructions.
    # However, standard practice allows both if it resolves correctly. Let's check absolute resolution.
    assert os.path.abspath(os.path.join(active_dir, db_target)) == "/home/user/app_data/versions/db_config_v2.conf", \
        f"db.conf points to incorrect target: {db_target}"

    # Verify keys.json symlink
    keys_json_path = os.path.join(active_dir, "keys.json")
    assert os.path.islink(keys_json_path), f"{keys_json_path} is not a symlink"
    keys_target = os.readlink(keys_json_path)
    assert os.path.abspath(os.path.join(active_dir, keys_target)) == "/home/user/app_data/versions/api_keys_v3.json", \
        f"keys.json points to incorrect target: {keys_target}"

def test_rebuild_log():
    log_path = "/home/user/rebuild.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Linked db.conf to db_config_v2.conf",
        "Linked keys.json to api_keys_v3.json"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected log entry missing: '{expected}'"

    assert len(lines) == 2, f"Log file contains unexpected entries. Found {len(lines)} lines, expected 2."

def test_backup_tarball():
    tar_path = "/home/user/backup/app_backup.tar.gz"
    assert os.path.isfile(tar_path), f"Backup tarball missing: {tar_path}"

    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getmembers()

        # Look for active/db.conf and active/keys.json
        # They might be prefixed with ./
        db_conf_member = None
        keys_json_member = None

        for m in members:
            if m.name.endswith("active/db.conf"):
                db_conf_member = m
            elif m.name.endswith("active/keys.json"):
                keys_json_member = m

        assert db_conf_member is not None, "active/db.conf not found in backup tarball"
        assert keys_json_member is not None, "active/keys.json not found in backup tarball"

        # Verify they are regular files (dereferenced), not symlinks
        assert db_conf_member.isfile(), f"{db_conf_member.name} in tarball is not a regular file (was it dereferenced?)"
        assert keys_json_member.isfile(), f"{keys_json_member.name} in tarball is not a regular file (was it dereferenced?)"

        # Verify content of db.conf
        f = tar.extractfile(db_conf_member)
        assert f is not None, "Could not extract db.conf from tarball"
        content = f.read().decode('utf-8').strip()
        assert content == "port=5433", f"Incorrect content in backed up db.conf: {content}"