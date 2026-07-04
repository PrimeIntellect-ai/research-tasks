# test_final_state.py

import os
import tarfile
import pytest

def test_log_sanitation():
    app_log_path = '/home/user/legacy_project/logs/app.log'
    debug_log_path = '/home/user/legacy_project/logs/old/debug.log'

    assert os.path.isfile(app_log_path), f"Log file {app_log_path} is missing."
    assert os.path.isfile(debug_log_path), f"Log file {debug_log_path} is missing."

    with open(app_log_path, 'r') as f:
        app_content = f.read()
        assert "[REDACTED]" in app_content, "Emails in app.log were not redacted."
        assert "admin@example.com" not in app_content, "admin@example.com was not redacted in app.log."
        assert "support@domain.co.uk" not in app_content, "support@domain.co.uk was not redacted in app.log."

    with open(debug_log_path, 'r') as f:
        debug_content = f.read()
        assert "[REDACTED]" in debug_content, "Emails in debug.log were not redacted."
        assert "test1@test.com" not in debug_content, "test1@test.com was not redacted in debug.log."
        assert "test.user@sub.domain.org" not in debug_content, "test.user@sub.domain.org was not redacted in debug.log."

def test_binary_categorization():
    elf_dir = '/home/user/legacy_project/organized/elf'
    png_dir = '/home/user/legacy_project/organized/png'
    unknown_dir = '/home/user/legacy_project/organized/unknown'
    assets_dir = '/home/user/legacy_project/assets'

    assert os.path.isfile(os.path.join(elf_dir, 'file1_bin')), "file1_bin was not moved to the elf directory."
    assert os.path.isfile(os.path.join(elf_dir, 'file4_bin')), "file4_bin was not moved to the elf directory."
    assert os.path.isfile(os.path.join(png_dir, 'file2_img')), "file2_img was not moved to the png directory."
    assert os.path.isfile(os.path.join(unknown_dir, 'file3_rand')), "file3_rand was not moved to the unknown directory."

    if os.path.isdir(assets_dir):
        assert len(os.listdir(assets_dir)) == 0, f"{assets_dir} should be empty after moving files."

def test_backups():
    full_backup = '/home/user/backups/backup_full.tar'
    inc_backup = '/home/user/backups/backup_inc.tar'
    snar_file = '/home/user/backups/project.snar'
    update_txt = '/home/user/legacy_project/organized/update.txt'

    assert os.path.isfile(full_backup), f"Full backup {full_backup} is missing."
    assert os.path.isfile(inc_backup), f"Incremental backup {inc_backup} is missing."
    assert os.path.isfile(snar_file), f"Snapshot file {snar_file} is missing."
    assert os.path.isfile(update_txt), f"Update file {update_txt} is missing."

    with open(update_txt, 'r') as f:
        assert f.read().strip() == "Backup test", "update.txt does not contain the correct text."

    # Check if update.txt is in the incremental backup
    found = False
    try:
        with tarfile.open(inc_backup, 'r') as tar:
            for member in tar.getmembers():
                if member.name.endswith('organized/update.txt'):
                    found = True
                    break
    except tarfile.TarError:
        pytest.fail(f"Could not read tar file {inc_backup}.")

    assert found, "The incremental backup does not contain the newly created update.txt file."