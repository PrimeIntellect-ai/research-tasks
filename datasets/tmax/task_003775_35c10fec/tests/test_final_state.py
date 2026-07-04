# test_final_state.py
import os
import json
import hashlib
import pytest

UPLOADS_DIR = "/home/user/uploads"
PROCESSED_DIR = "/home/user/processed"
EXTRACTED_DIR = os.path.join(PROCESSED_DIR, "extracted")
DELETED_LOG = os.path.join(PROCESSED_DIR, "deleted.log")
MANIFEST_FILE = os.path.join(PROCESSED_DIR, "manifest.json")

def test_deleted_log_contents():
    assert os.path.isfile(DELETED_LOG), f"Missing deleted log file: {DELETED_LOG}"
    with open(DELETED_LOG, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["bad_actor.tar.gz", "mixed.zip"]
    assert lines == expected_lines, f"Expected {DELETED_LOG} to contain exactly {expected_lines} in alphabetical order, but got {lines}"

def test_malicious_archives_deleted():
    for filename in ["bad_actor.tar.gz", "mixed.zip"]:
        path = os.path.join(UPLOADS_DIR, filename)
        assert not os.path.exists(path), f"Malicious archive {path} was not deleted from uploads directory."

def test_safe_archives_exist():
    for filename in ["safe_data.zip", "safe_archive.tar.gz"]:
        path = os.path.join(UPLOADS_DIR, filename)
        assert os.path.isfile(path), f"Safe archive {path} should not have been deleted."

def test_extracted_files_content_and_encoding():
    assert os.path.isdir(EXTRACTED_DIR), f"Missing extracted directory: {EXTRACTED_DIR}"

    # Check notes.txt
    notes_path = os.path.join(EXTRACTED_DIR, "notes.txt")
    assert os.path.isfile(notes_path), f"Missing extracted file: {notes_path}"
    with open(notes_path, "rb") as f:
        notes_content = f.read()
    assert notes_content == "München".encode("utf-8"), f"notes.txt was not correctly converted to UTF-8. Got {notes_content!r}"

    # Check docs/report.txt
    report_path = os.path.join(EXTRACTED_DIR, "docs", "report.txt")
    assert os.path.isfile(report_path), f"Missing extracted file: {report_path}"
    with open(report_path, "rb") as f:
        report_content = f.read()
    assert report_content == "Voilà".encode("utf-8"), f"docs/report.txt was not correctly converted to UTF-8. Got {report_content!r}"

    # Check data/stats.bin
    stats_path = os.path.join(EXTRACTED_DIR, "data", "stats.bin")
    assert os.path.isfile(stats_path), f"Missing extracted file: {stats_path}"
    with open(stats_path, "rb") as f:
        stats_content = f.read()
    assert stats_content == b'\x00\x01\x02\x03', f"data/stats.bin was improperly modified. Got {stats_content!r}"

def test_manifest_json():
    assert os.path.isfile(MANIFEST_FILE), f"Missing manifest file: {MANIFEST_FILE}"
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest file {MANIFEST_FILE} is not valid JSON.")

    expected_manifest = {
        "notes.txt": hashlib.sha256("München".encode("utf-8")).hexdigest(),
        "data/stats.bin": hashlib.sha256(b'\x00\x01\x02\x03').hexdigest(),
        "docs/report.txt": hashlib.sha256("Voilà".encode("utf-8")).hexdigest()
    }

    assert manifest == expected_manifest, f"Manifest content does not match expected output. Got: {manifest}"