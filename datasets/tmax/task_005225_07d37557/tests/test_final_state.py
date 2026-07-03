# test_final_state.py
import os
import tarfile
import difflib
import pytest
import shutil

EXPECTED_TEXT = "Please add a section about the new OAuth2 authentication flow and ensure the legacy login tokens are marked as deprecated."

def test_incremental_archive_exists():
    archive_path = "/home/user/incremental.tar.gz"
    assert os.path.exists(archive_path), f"Incremental archive not found at {archive_path}"
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive"

def test_incremental_archive_contents_and_transcription():
    archive_path = "/home/user/incremental.tar.gz"
    extract_dir = "/tmp/verify_pytest"

    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir, exist_ok=True)

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()
        # Should contain exactly one file (ignoring directories if any, but the task says "only the documentation files")
        file_members = [m for m in members if m.isfile()]

        assert len(file_members) == 1, f"Archive should contain exactly 1 modified file, found {len(file_members)}"
        assert file_members[0].name.endswith("auth.md"), f"Archived file should be auth.md, found {file_members[0].name}"

        tar.extractall(extract_dir)
        extracted_file_path = os.path.join(extract_dir, file_members[0].name)

        with open(extracted_file_path, "r") as f:
            lines = f.read().strip().split('\n')

        assert len(lines) > 0, "The archived auth.md file is empty"
        actual_text = lines[-1]

        ratio = difflib.SequenceMatcher(None, EXPECTED_TEXT.lower(), actual_text.lower()).ratio()
        assert ratio >= 0.75, f"Transcription similarity metric {ratio:.2f} is below threshold 0.75. Expected: '{EXPECTED_TEXT}', Actual: '{actual_text}'"

def test_original_file_modified():
    # Also verify that the file in /home/user/docs/auth.md was modified
    auth_doc_path = "/home/user/docs/auth.md"
    assert os.path.exists(auth_doc_path), f"Extracted document not found at {auth_doc_path}"

    with open(auth_doc_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0, "The auth.md file in docs is empty"
    actual_text = lines[-1]

    ratio = difflib.SequenceMatcher(None, EXPECTED_TEXT.lower(), actual_text.lower()).ratio()
    assert ratio >= 0.75, f"Transcription similarity metric in docs/auth.md {ratio:.2f} is below threshold 0.75."