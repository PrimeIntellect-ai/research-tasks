# test_final_state.py
import os
import json
import pytest

def test_bare_repo_exists():
    """Verify that the bare Git repository was created."""
    repo_config = '/home/user/backup_vault.git/config'
    assert os.path.exists(repo_config), "Bare repository not found at /home/user/backup_vault.git."

def test_post_receive_hook():
    """Verify that the post-receive hook exists and is executable."""
    hook_path = '/home/user/backup_vault.git/hooks/post-receive'
    assert os.path.exists(hook_path), f"post-receive hook not found at {hook_path}."
    assert os.access(hook_path, os.X_OK), f"post-receive hook at {hook_path} is not executable."

def test_restores_latest_symlink():
    """Verify that the latest restore symlink exists and points to a directory."""
    latest_link = '/home/user/restores/latest'
    assert os.path.islink(latest_link), f"{latest_link} is not a symlink."
    target_dir = os.readlink(latest_link)
    # The symlink might be relative or absolute, but resolving it should point to an existing dir
    resolved_target = os.path.realpath(latest_link)
    assert os.path.isdir(resolved_target), f"Symlink {latest_link} does not point to a valid directory."

def test_manifest_in_latest_restore():
    """Verify that the manifest exists in the latest restore directory and has correct contents."""
    manifest_path = '/home/user/restores/latest/restore_manifest.json'
    assert os.path.exists(manifest_path), f"restore_manifest.json not found at {manifest_path}."

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("restore_manifest.json is not valid JSON.")

    assert manifest.get("archive") == "db_backup_v9.tar.gz", "Incorrect archive value in manifest."
    assert manifest.get("mount_target") == "/home/user/mnt/recovery_db", "Incorrect mount_target value in manifest."

def test_mock_fstab_updated():
    """Verify that mock_fstab contains the expected entry."""
    fstab_path = '/home/user/mock_fstab'
    assert os.path.exists(fstab_path), f"mock_fstab not found at {fstab_path}."

    with open(fstab_path, 'r') as f:
        fstab_contents = f.read()

    expected_entry = "db_backup_v9.tar.gz /home/user/mnt/recovery_db auto defaults 0 0"
    assert expected_entry in fstab_contents, f"mock_fstab does not contain the expected mount entry: '{expected_entry}'"

def test_verification_script_exists():
    """Verify the interactive verification script exists."""
    script_path = '/home/user/verify_restore.py'
    assert os.path.exists(script_path), f"verify_restore.py not found at {script_path}."

def test_restore_test_log():
    """Verify that the restore test log contains the expected success message."""
    log_path = '/home/user/restore_test.log'
    assert os.path.exists(log_path), f"restore_test.log not found at {log_path}."

    with open(log_path, 'r') as f:
        log_contents = f.read()

    expected_log = "SUCCESS: Restore registered for db_backup_v9.tar.gz at /home/user/mnt/recovery_db"
    assert expected_log in log_contents, f"restore_test.log does not contain the expected success message: '{expected_log}'"