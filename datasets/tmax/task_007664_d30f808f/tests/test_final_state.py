# test_final_state.py
import os
import tarfile
import json

def test_symlinks_removed():
    loop_dir = "/home/user/project_rescue/src/assets/loop_dir"
    root_link = "/home/user/project_rescue/src/subdir/root_link"

    assert not os.path.exists(loop_dir) and not os.path.islink(loop_dir), f"Symlink {loop_dir} was not removed."
    assert not os.path.exists(root_link) and not os.path.islink(root_link), f"Symlink {root_link} was not removed."

def test_archives_integrity_checked():
    corrupt_archive = "/home/user/project_rescue/archives/backup_corrupt.tar.gz"
    valid_archive = "/home/user/project_rescue/archives/backup_valid.tar.gz"

    assert not os.path.exists(corrupt_archive), f"Corrupted archive {corrupt_archive} was not deleted."
    assert os.path.exists(valid_archive), f"Valid archive {valid_archive} should not have been deleted."
    assert tarfile.is_tarfile(valid_archive), f"{valid_archive} should still be a valid tar file."

def test_config_file_updated():
    config_file = "/home/user/project_rescue/config/settings.yaml"
    assert os.path.exists(config_file), f"Config file {config_file} is missing."

    with open(config_file, 'r') as f:
        content = f.read()

    assert "BAD_PATH_PREFIX_992" not in content, "The bad path prefix 'BAD_PATH_PREFIX_992' was not completely removed from the config file."
    assert "/home/user/project_rescue/src/data" in content, "The correct path '/home/user/project_rescue/src' was not properly substituted into the config file."

def test_smart_backup_script_exists():
    script_path = "/home/user/project_rescue/smart_backup.py"
    assert os.path.exists(script_path), f"Backup script {script_path} does not exist."

def test_backup_report_json():
    report_path = "/home/user/project_rescue/backup_report.json"
    assert os.path.exists(report_path), f"Backup report {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Report {report_path} is not valid JSON."

    assert "backed_up_files" in report, "Report is missing 'backed_up_files' key."
    assert "ignored_symlinks" in report, "Report is missing 'ignored_symlinks' key."

    expected_files = ["new_file.py", "subdir/new_data.txt"]
    actual_files = sorted(report["backed_up_files"])
    assert actual_files == sorted(expected_files), f"Expected backed_up_files to be {expected_files}, got {actual_files}."

    # Since symlinks were deleted in step 1, ignored_symlinks should be empty
    assert isinstance(report["ignored_symlinks"], list), "'ignored_symlinks' should be a list."
    assert len(report["ignored_symlinks"]) == 0, f"Expected ignored_symlinks to be empty, got {report['ignored_symlinks']}."

def test_incremental_backup_archive():
    archive_path = "/home/user/project_rescue/archives/incremental_backup.tar.gz"
    assert os.path.exists(archive_path), f"Incremental backup archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar file."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()

    # Check that expected files are in the archive
    # The paths should be relative to src/
    expected_files = ["new_file.py", "subdir/new_data.txt"]
    for ef in expected_files:
        # Accept either exact relative path or prefixed with './'
        assert ef in members or f"./{ef}" in members, f"Expected file {ef} not found in the backup archive."

    # Ensure old_file.py is NOT in the archive
    assert "old_file.py" not in members and "./old_file.py" not in members, "old_file.py was incorrectly included in the incremental backup."