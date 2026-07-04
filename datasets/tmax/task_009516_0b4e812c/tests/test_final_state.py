# test_final_state.py
import os
import struct
import pytest

BASE_DIR = "/home/user/legacy_docs"
REPORT_PATH = "/home/user/asset_report.csv"

def get_bdoc_data():
    bdoc_data = {}
    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".bdoc"):
                full_path = os.path.join(root, file)
                with open(full_path, "rb") as f:
                    magic = f.read(4)
                    if magic == b"BDOC":
                        asset_id = struct.unpack("<I", f.read(4))[0]
                        ts = struct.unpack("<Q", f.read(8))[0]
                        bdoc_data[file] = {"asset_id": asset_id, "timestamp": ts}
    return bdoc_data

def test_csv_report():
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"

    bdoc_data = get_bdoc_data()
    expected_rows = ["filename,AssetID,Timestamp"]
    for filename in sorted(bdoc_data.keys()):
        data = bdoc_data[filename]
        expected_rows.append(f"{filename},{data['asset_id']},{data['timestamp']}")

    expected_csv = "\n".join(expected_rows)

    with open(REPORT_PATH, "r") as f:
        actual_csv = f.read().strip()

    # Compare line by line to give better error messages
    actual_lines = actual_csv.splitlines()
    expected_lines = expected_csv.splitlines()

    assert len(actual_lines) == len(expected_lines), f"CSV line count mismatch. Expected {len(expected_lines)}, got {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"CSV mismatch on line {i+1}. Expected '{expected}', got '{actual}'"

def test_markdown_files_updated():
    bdoc_data = get_bdoc_data()

    # Instead of hardcoding the expected text, we verify that the known files have the correct replacements.
    md1 = os.path.join(BASE_DIR, "section1/intro.md")
    assert os.path.isfile(md1), f"Markdown file {md1} is missing"

    with open(md1, "r") as f:
        content1 = f.read()

    assert "[[ASSET_REF" not in content1, f"Unreplaced macro found in {md1}"
    assert f"[Asset ID: {bdoc_data['diagram.bdoc']['asset_id']}](diagram.bdoc)" in content1, f"Correct replacement missing in {md1}"

    md2 = os.path.join(BASE_DIR, "section2/deep/details.md")
    assert os.path.isfile(md2), f"Markdown file {md2} is missing"

    with open(md2, "r") as f:
        content2 = f.read()

    assert "[[ASSET_REF" not in content2, f"Unreplaced macro found in {md2}"
    assert f"[Asset ID: {bdoc_data['flow.bdoc']['asset_id']}](flow.bdoc)" in content2, f"Correct replacement for flow.bdoc missing in {md2}"
    assert f"[Asset ID: {bdoc_data['architecture.bdoc']['asset_id']}](architecture.bdoc)" in content2, f"Correct replacement for architecture.bdoc missing in {md2}"

def test_no_unreplaced_macros():
    # Ensure no other markdown files have unreplaced macros
    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                with open(full_path, "r") as f:
                    content = f.read()
                    assert "[[ASSET_REF:" not in content, f"Found unreplaced macro in {full_path}"