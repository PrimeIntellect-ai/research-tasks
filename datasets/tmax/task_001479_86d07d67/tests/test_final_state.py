# test_final_state.py

import os
import json
import hashlib
import csv
import pytest

def get_expected_state():
    config_path = "/home/user/config.json"
    manifest_path = "/home/user/manifest.json"

    with open(config_path, "r") as f:
        config = json.load(f)
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    allowed_base_dir = config.get("allowed_base_dir", "/home/user/extracted")
    max_total_bytes = config.get("max_total_bytes", 500)

    expected_files = {}
    total_bytes = 0

    for item in manifest:
        path = item.get("path", "")
        content = item.get("content", "")

        # Security rules: skip if contains '..' or starts with '/'
        if ".." in path or path.startswith("/"):
            continue

        content_bytes = content.encode('utf-8')

        # Quota rule: skip this and all subsequent if max_total_bytes is exceeded
        if total_bytes + len(content_bytes) > max_total_bytes:
            break

        expected_files[path] = content_bytes
        total_bytes += len(content_bytes)

    return allowed_base_dir, expected_files

def test_extracted_files():
    allowed_base_dir, expected_files = get_expected_state()

    assert os.path.isdir(allowed_base_dir), f"Directory {allowed_base_dir} does not exist."

    # Check that all expected files exist and have correct content
    for rel_path, expected_content in expected_files.items():
        full_path = os.path.join(allowed_base_dir, rel_path)
        assert os.path.isfile(full_path), f"Expected file missing: {full_path}"

        with open(full_path, "rb") as f:
            actual_content = f.read()
        assert actual_content == expected_content, f"Content mismatch in {full_path}"

def test_no_extra_files():
    allowed_base_dir, expected_files = get_expected_state()

    # Check that NO extra files exist in the allowed_base_dir
    actual_files = []
    for root, _, files in os.walk(allowed_base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, allowed_base_dir)
            actual_files.append(rel_path)

    for rel_path in actual_files:
        assert rel_path in expected_files, f"Unexpected file found in extracted directory: {rel_path}"

def test_extraction_report():
    _, expected_files = get_expected_state()
    report_path = "/home/user/extraction_report.csv"

    assert os.path.isfile(report_path), f"Extraction report missing at {report_path}"

    expected_csv_rows = {}
    for rel_path, content in expected_files.items():
        sha256_hash = hashlib.sha256(content).hexdigest()
        expected_csv_rows[rel_path] = sha256_hash

    actual_csv_rows = {}
    with open(report_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["filepath", "sha256"], f"Invalid CSV header in {report_path}: {header}"

        for row in reader:
            if not row:
                continue
            assert len(row) == 2, f"Invalid CSV row format: {row}"
            actual_csv_rows[row[0]] = row[1]

    assert actual_csv_rows == expected_csv_rows, "Extraction report contents do not match expected successfully written files and checksums."