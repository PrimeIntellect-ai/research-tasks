# test_final_state.py

import os
import csv
import hashlib
import json
import pytest

RAW_ASSETS_DIR = "/home/user/project/raw_assets"
PROCESSED_DIR = "/home/user/project/processed_assets"
MANIFEST_PATH = "/home/user/project/manifest.csv"

EXPECTED_FILES = {
    "hero_banner.webp": "Hero Banner.jpg",
    "server_config.yaml": "Server-Config.json",
    "ui_settings.yaml": "UI Settings.json",
    "user_avatar_01.webp": "User-Avatar 01.PNG"
}

def test_processed_directory_and_files():
    assert os.path.exists(PROCESSED_DIR), f"Processed directory missing: {PROCESSED_DIR}"
    assert os.path.isdir(PROCESSED_DIR), f"Not a directory: {PROCESSED_DIR}"

    actual_files = set(os.listdir(PROCESSED_DIR))
    expected_files = set(EXPECTED_FILES.keys())

    assert actual_files == expected_files, f"Expected files {expected_files}, but got {actual_files}"

def test_webp_format():
    for filename in ["hero_banner.webp", "user_avatar_01.webp"]:
        filepath = os.path.join(PROCESSED_DIR, filename)
        assert os.path.exists(filepath), f"Missing file: {filepath}"

        with open(filepath, "rb") as f:
            header = f.read(12)

        assert len(header) >= 12, f"File too small to be WebP: {filename}"
        assert header[0:4] == b"RIFF", f"Missing RIFF header in {filename}"
        assert header[8:12] == b"WEBP", f"Missing WEBP signature in {filename}"

def test_yaml_content():
    # We use basic string checks since PyYAML is not in stdlib
    server_config_path = os.path.join(PROCESSED_DIR, "server_config.yaml")
    assert os.path.exists(server_config_path), f"Missing file: {server_config_path}"
    with open(server_config_path, "r") as f:
        content = f.read()
        assert "localhost" in content, "Missing 'localhost' in server_config.yaml"
        assert "8080" in content, "Missing '8080' in server_config.yaml"
        assert "auth" in content, "Missing 'auth' in server_config.yaml"
        assert "logging" in content, "Missing 'logging' in server_config.yaml"

    ui_settings_path = os.path.join(PROCESSED_DIR, "ui_settings.yaml")
    assert os.path.exists(ui_settings_path), f"Missing file: {ui_settings_path}"
    with open(ui_settings_path, "r") as f:
        content = f.read()
        assert "dark" in content, "Missing 'dark' in ui_settings.yaml"
        assert "false" in content.lower(), "Missing 'false' in ui_settings.yaml"

def test_manifest_exists_and_format():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file missing: {MANIFEST_PATH}"

    with open(MANIFEST_PATH, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Manifest is empty"
    assert rows[0] == ["processed_filename", "original_filename", "sha256"], \
        f"Incorrect CSV header. Got: {rows[0]}"

    data_rows = rows[1:]
    assert len(data_rows) == 4, f"Expected 4 data rows, got {len(data_rows)}"

    processed_names = [row[0] for row in data_rows]
    assert processed_names == sorted(processed_names), "Manifest rows are not sorted alphabetically by processed_filename"

    for row in data_rows:
        assert len(row) == 3, f"Row does not have exactly 3 columns: {row}"
        p_file, o_file, file_hash = row

        assert p_file in EXPECTED_FILES, f"Unexpected processed filename in manifest: {p_file}"
        assert EXPECTED_FILES[p_file] == o_file, f"Incorrect original filename mapping for {p_file}. Expected {EXPECTED_FILES[p_file]}, got {o_file}"

        filepath = os.path.join(PROCESSED_DIR, p_file)
        assert os.path.exists(filepath), f"File referenced in manifest does not exist: {filepath}"

        with open(filepath, "rb") as f_img:
            actual_hash = hashlib.sha256(f_img.read()).hexdigest()

        assert actual_hash == file_hash, f"SHA256 hash mismatch for {p_file}. Expected {actual_hash}, got {file_hash}"

def test_raw_assets_unmodified():
    expected_raw_files = ["Hero Banner.jpg", "Server-Config.json", "UI Settings.json", "User-Avatar 01.PNG"]
    assert os.path.exists(RAW_ASSETS_DIR), f"Raw assets directory missing: {RAW_ASSETS_DIR}"

    actual_raw_files = os.listdir(RAW_ASSETS_DIR)
    for f in expected_raw_files:
        assert f in actual_raw_files, f"Original file missing from raw_assets: {f}"