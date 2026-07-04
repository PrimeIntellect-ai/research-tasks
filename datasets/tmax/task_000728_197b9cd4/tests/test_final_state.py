# test_final_state.py

import os
import json
import csv
import pytest

RAW_DATASET_DIR = "/home/user/raw_dataset"
CLEAN_DATASET_DIR = "/home/user/clean_dataset"
CORRUPT_ARCHIVES_DIR = "/home/user/corrupt_archives"
MANIFEST_FILE = "/home/user/clean_dataset_manifest.txt"

def test_directories_created():
    assert os.path.isdir(CLEAN_DATASET_DIR), f"Directory {CLEAN_DATASET_DIR} was not created."
    assert os.path.isdir(CORRUPT_ARCHIVES_DIR), f"Directory {CORRUPT_ARCHIVES_DIR} was not created."

def test_symlinks_handled():
    link1 = f"{RAW_DATASET_DIR}/loop_dir/link1"
    link2 = f"{RAW_DATASET_DIR}/loop_dir/link2"
    valid_link = f"{RAW_DATASET_DIR}/exp_a/valid_link.txt"

    assert not os.path.lexists(link1), f"Broken symlink {link1} was not deleted."
    assert not os.path.lexists(link2), f"Broken symlink {link2} was not deleted."
    assert os.path.islink(valid_link), f"Valid symlink {valid_link} should not be deleted."
    assert os.path.exists(valid_link), f"Valid symlink {valid_link} is broken."

def test_archives_handled():
    valid_zip = f"{RAW_DATASET_DIR}/exp_a/data.zip"
    valid_tar = f"{RAW_DATASET_DIR}/exp_b/nested/archive.tar.gz"
    corrupt_zip_orig = f"{RAW_DATASET_DIR}/exp_b/bad_data.zip"
    corrupt_tar_orig = f"{RAW_DATASET_DIR}/exp_b/nested/broken.tar.gz"

    corrupt_zip_dest = f"{CORRUPT_ARCHIVES_DIR}/bad_data.zip"
    corrupt_tar_dest = f"{CORRUPT_ARCHIVES_DIR}/broken.tar.gz"

    assert os.path.isfile(valid_zip), f"Valid archive {valid_zip} should remain in place."
    assert os.path.isfile(valid_tar), f"Valid archive {valid_tar} should remain in place."

    assert not os.path.exists(corrupt_zip_orig), f"Corrupt archive {corrupt_zip_orig} was not moved."
    assert not os.path.exists(corrupt_tar_orig), f"Corrupt archive {corrupt_tar_orig} was not moved."

    assert os.path.isfile(corrupt_zip_dest), f"Corrupt archive was not moved to {corrupt_zip_dest}."
    assert os.path.isfile(corrupt_tar_dest), f"Corrupt archive was not moved to {corrupt_tar_dest}."

def test_json_to_csv_conversion():
    json_files = [
        f"{RAW_DATASET_DIR}/exp_a/measurements",
        f"{RAW_DATASET_DIR}/exp_b/nested/stats"
    ]

    for base_path in json_files:
        json_path = f"{base_path}.json"
        csv_path = f"{base_path}.csv"

        assert os.path.isfile(json_path), f"Original JSON file {json_path} should not be deleted."
        assert os.path.isfile(csv_path), f"CSV file {csv_path} was not created."

        with open(json_path, 'r') as jf:
            data = json.load(jf)

        with open(csv_path, 'r') as cf:
            reader = csv.reader(cf)
            rows = list(reader)

        assert len(rows) > 0, f"CSV file {csv_path} is empty."
        assert [r.strip() for r in rows[0]] == ["id", "value"], f"CSV header in {csv_path} is incorrect."

        # Verify data rows
        assert len(rows) - 1 == len(data), f"CSV row count does not match JSON array length in {csv_path}."
        for i, obj in enumerate(data):
            csv_row = [r.strip() for r in rows[i+1]]
            # strip quotes if any
            csv_id = csv_row[0].strip('"\'')
            csv_value = csv_row[1].strip('"\'')
            assert str(obj["id"]) == csv_id, f"ID mismatch in {csv_path} row {i+1}."
            assert str(obj["value"]) == csv_value, f"Value mismatch in {csv_path} row {i+1}."

def test_hard_links_created():
    expected_links = {
        f"{RAW_DATASET_DIR}/exp_a/measurements.csv": f"{CLEAN_DATASET_DIR}/exp_a_measurements.csv",
        f"{RAW_DATASET_DIR}/exp_b/nested/stats.csv": f"{CLEAN_DATASET_DIR}/nested_stats.csv",
        f"{RAW_DATASET_DIR}/exp_b/existing.csv": f"{CLEAN_DATASET_DIR}/exp_b_existing.csv"
    }

    for orig_path, link_path in expected_links.items():
        assert os.path.isfile(orig_path), f"Original CSV file {orig_path} is missing."
        assert os.path.isfile(link_path), f"Hard link {link_path} was not created."

        orig_stat = os.stat(orig_path)
        link_stat = os.stat(link_path)

        assert orig_stat.st_ino == link_stat.st_ino, f"{link_path} is not a hard link to {orig_path}."

def test_manifest_file():
    assert os.path.isfile(MANIFEST_FILE), f"Manifest file {MANIFEST_FILE} was not created."

    with open(MANIFEST_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = sorted([
        "exp_a_measurements.csv",
        "exp_b_existing.csv",
        "nested_stats.csv"
    ])

    assert lines == expected_lines, f"Manifest file contents do not match expected sorted output. Got {lines}"