# test_final_state.py

import os
import hashlib
import pytest

EXTRACTED_DIR = "/home/user/extracted"
MANIFEST_PATH = "/home/user/manifest.txt"
VULN_TARGET_PATH = "/home/user/secret.txt"

def test_zip_slip_mitigated():
    """Verify that the path traversal attempt was mitigated and not extracted to the vulnerable path."""
    assert not os.path.exists(VULN_TARGET_PATH), (
        f"Zip slip vulnerability was exploited! Found file at {VULN_TARGET_PATH}"
    )

def test_secret_txt_extracted_safely():
    """Verify that secret.txt was extracted to the safe directory with correct UTF-8 content."""
    safe_path = os.path.join(EXTRACTED_DIR, "secret.txt")
    assert os.path.exists(safe_path), f"Expected extracted file not found at {safe_path}"

    with open(safe_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == "秘密のデータ", f"Content of {safe_path} is incorrect."

def test_records_csv_extracted():
    """Verify that records.csv was extracted with correct UTF-8 content."""
    # It might be in valid_data/records.csv or just records.csv depending on how the student handled safe paths
    path1 = os.path.join(EXTRACTED_DIR, "valid_data", "records.csv")
    path2 = os.path.join(EXTRACTED_DIR, "records.csv")

    actual_path = None
    if os.path.exists(path1):
        actual_path = path1
    elif os.path.exists(path2):
        actual_path = path2

    assert actual_path is not None, f"records.csv not found in {EXTRACTED_DIR} or {os.path.join(EXTRACTED_DIR, 'valid_data')}"

    with open(actual_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == "名前,年齢", f"Content of {actual_path} is incorrect."

def test_no_tmp_files_left_behind():
    """Verify that no .tmp files are left in the extracted directory."""
    for root, _, files in os.walk(EXTRACTED_DIR):
        for file in files:
            assert not file.endswith(".tmp"), f"Temporary file left behind: {os.path.join(root, file)}"

def test_manifest_exists_and_correct():
    """Verify the manifest file exists, is correctly formatted, and sorted."""
    assert os.path.exists(MANIFEST_PATH), f"Manifest file not found at {MANIFEST_PATH}"

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Manifest should contain exactly 2 lines, found {len(lines)}"

    # Expected hashes for the UTF-8 content
    # "名前,年齢" encoded in utf-8
    records_hash = hashlib.sha256("名前,年齢".encode("utf-8")).hexdigest()
    # "秘密のデータ" encoded in utf-8
    secret_hash = hashlib.sha256("秘密のデータ".encode("utf-8")).hexdigest()

    expected_line1 = f"{records_hash}  records.csv"
    expected_line2 = f"{secret_hash}  secret.txt"

    assert lines[0] == expected_line1, f"Manifest line 1 incorrect. Expected '{expected_line1}', got '{lines[0]}'"
    assert lines[1] == expected_line2, f"Manifest line 2 incorrect. Expected '{expected_line2}', got '{lines[1]}'"