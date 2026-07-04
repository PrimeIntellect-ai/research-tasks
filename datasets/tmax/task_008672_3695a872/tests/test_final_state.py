# test_final_state.py
import os
import hashlib
import pytest

DUMP_DIR = "/home/user/project_dump"

def test_old_files_removed():
    old_files = ["logo.dat", "archive.tmp", "document", "notes.bin"]
    for f in old_files:
        path = os.path.join(DUMP_DIR, f)
        assert not os.path.exists(path), f"Old file {path} should have been renamed/removed."

def test_new_files_exist():
    new_files = ["archive.gz", "document.pdf", "logo.png", "notes.txt"]
    for f in new_files:
        path = os.path.join(DUMP_DIR, f)
        assert os.path.isfile(path), f"Expected new file {path} is missing. Was it correctly renamed?"

def test_manifest_exists_and_correct():
    manifest_path = os.path.join(DUMP_DIR, "manifest.sha256")
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    new_files = ["archive.gz", "document.pdf", "logo.png", "notes.txt"]
    expected_lines = []

    for f in sorted(new_files):
        path = os.path.join(DUMP_DIR, f)
        # We only compute checksum if the file exists to avoid crashing the test 
        # if the previous test failed, though pytest will report this anyway.
        if os.path.isfile(path):
            with open(path, "rb") as file_obj:
                checksum = hashlib.sha256(file_obj.read()).hexdigest()
            expected_lines.append(f"{checksum}  {f}")

    expected_content = "\n".join(expected_lines)

    with open(manifest_path, "r", encoding="utf-8") as m:
        actual_content = m.read().strip()

    assert actual_content == expected_content, "Manifest contents do not match expected checksums, format, or sorting."