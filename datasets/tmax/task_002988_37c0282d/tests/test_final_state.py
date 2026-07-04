# test_final_state.py

import os
import tarfile
import pytest

def test_directories_exist():
    """Test that the required directories have been created based on the config."""
    assert os.path.isdir("/home/user/incoming"), "/home/user/incoming is missing."
    assert os.path.isdir("/home/user/processed"), "/home/user/processed is missing."
    assert os.path.isdir("/home/user/archives"), "/home/user/archives is missing."

def test_converted_files_exist_and_correct_content():
    """Test that .md files were converted to .txt with correct content replacements."""
    intro_txt = "/home/user/processed/intro.txt"
    conclusion_txt = "/home/user/processed/conclusion.txt"

    assert os.path.isfile(intro_txt), f"{intro_txt} is missing."
    assert os.path.isfile(conclusion_txt), f"{conclusion_txt} is missing."

    with open(intro_txt, "r") as f:
        intro_content = f.read()
    assert "HEADER: Introduction" in intro_content, "intro.txt does not contain the replaced header."
    assert "Welcome to the docs." in intro_content, "intro.txt is missing original content."

    with open(conclusion_txt, "r") as f:
        conclusion_content = f.read()
    assert "HEADER: Conclusion" in conclusion_content, "conclusion.txt does not contain the replaced header."
    assert "End of docs." in conclusion_content, "conclusion.txt is missing original content."

def test_original_md_files_deleted():
    """Test that the original .md files were deleted from the processed directory."""
    assert not os.path.exists("/home/user/processed/intro.md"), "intro.md was not deleted."
    assert not os.path.exists("/home/user/processed/conclusion.md"), "conclusion.md was not deleted."

def test_changelog_exists():
    """Test that changelog.txt was created with correct content."""
    changelog_txt = "/home/user/processed/changelog.txt"
    assert os.path.isfile(changelog_txt), f"{changelog_txt} is missing."

    with open(changelog_txt, "r") as f:
        content = f.read().strip()
    assert content == "NEW UPDATE", "changelog.txt content is incorrect."

def test_backup_0_tar():
    """Test that backup_0.tar exists and contains the correct files."""
    backup_0 = "/home/user/archives/backup_0.tar"
    assert os.path.isfile(backup_0), f"{backup_0} is missing."

    with tarfile.open(backup_0, "r") as tar:
        names = tar.getnames()
        # tar files might contain paths like 'home/user/processed/intro.txt' or 'processed/intro.txt' or 'intro.txt'
        # We'll check if the filenames are present in the archive
        assert any(name.endswith("intro.txt") for name in names), "intro.txt is missing from backup_0.tar."
        assert any(name.endswith("conclusion.txt") for name in names), "conclusion.txt is missing from backup_0.tar."
        assert not any(name.endswith("changelog.txt") for name in names), "changelog.txt should not be in backup_0.tar."

def test_backup_1_tar():
    """Test that backup_1.tar exists and contains ONLY the incremental update."""
    backup_1 = "/home/user/archives/backup_1.tar"
    assert os.path.isfile(backup_1), f"{backup_1} is missing."

    with tarfile.open(backup_1, "r") as tar:
        names = tar.getnames()
        assert any(name.endswith("changelog.txt") for name in names), "changelog.txt is missing from backup_1.tar."
        # The incremental backup shouldn't contain the full contents of intro.txt/conclusion.txt
        # GNU tar incremental backups might list directories, but we ensure the files aren't archived again.
        # Check that members are not regular files for intro.txt/conclusion.txt
        for member in tar.getmembers():
            if member.name.endswith("intro.txt") or member.name.endswith("conclusion.txt"):
                assert not member.isfile(), f"{member.name} was fully archived in incremental backup_1.tar."

def test_snapshot_file_exists():
    """Test that the snapshot file exists."""
    snapshot = "/home/user/archives/backup.snar"
    assert os.path.isfile(snapshot), f"Snapshot file {snapshot} is missing."