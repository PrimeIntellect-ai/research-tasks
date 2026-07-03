# test_final_state.py

import os
import json
import hashlib
import sqlite3
import xml.etree.ElementTree as ET

BASE_DIR = "/home/user/mobile_pipeline"
SO_PATH = os.path.join(BASE_DIR, "build", "libcore.so")
MANIFEST_PATH = os.path.join(BASE_DIR, "manifest.json")
DB_PATH = os.path.join(BASE_DIR, "ota.db")
XML_PATH = os.path.join(BASE_DIR, "metadata.xml")

def get_expected_metadata():
    tree = ET.parse(XML_PATH)
    root = tree.getroot()
    version = root.find("version").text
    target = root.find("target").text
    return version, target

def get_file_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_build_success():
    """Test that the C library was built successfully."""
    assert os.path.isfile(SO_PATH), f"Shared object file {SO_PATH} was not built. Did 'make' succeed?"

def test_manifest_json():
    """Test that manifest.json is created with correct values."""
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist."

    with open(MANIFEST_PATH, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            assert False, "manifest.json is not a valid JSON file."

    expected_version, expected_target = get_expected_metadata()
    expected_sha256 = get_file_sha256(SO_PATH)

    assert manifest.get("version") == expected_version, f"Expected version '{expected_version}' in manifest, got '{manifest.get('version')}'"
    assert manifest.get("file") == expected_target, f"Expected file '{expected_target}' in manifest, got '{manifest.get('file')}'"
    assert manifest.get("sha256") == expected_sha256, f"Expected sha256 '{expected_sha256}' in manifest, got '{manifest.get('sha256')}'"

def test_database_schema_and_data():
    """Test that ota.db schema is migrated and the new record is inserted."""
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check schema
    cursor.execute("PRAGMA table_info(releases);")
    columns = {row[1]: row[2] for row in cursor.fetchall()}

    assert "checksum" in columns, "Column 'checksum' was not added to the releases table."
    assert "status" in columns, "Column 'status' was not added to the releases table."

    # Check data
    expected_version, expected_target = get_expected_metadata()
    expected_sha256 = get_file_sha256(SO_PATH)

    cursor.execute("SELECT target, checksum, status FROM releases WHERE version=?;", (expected_version,))
    row = cursor.fetchone()

    assert row is not None, f"No record found in releases table for version '{expected_version}'."
    assert row[0] == expected_target, f"Expected target '{expected_target}' in DB, got '{row[0]}'."
    assert row[1] == expected_sha256, f"Expected checksum '{expected_sha256}' in DB, got '{row[1]}'."
    assert row[2] == "pending", f"Expected status 'pending' in DB, got '{row[2]}'."

    conn.close()