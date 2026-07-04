# test_final_state.py

import os
import csv
import hashlib

def test_organized_docs_directory_exists():
    assert os.path.isdir("/home/user/organized_docs"), "/home/user/organized_docs directory is missing"

def test_manifest_exists_and_format():
    manifest_path = "/home/user/organized_docs/manifest.csv"
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "manifest.csv is empty"

    headers = rows[0]
    expected_headers = ["Title", "RelativePath", "SHA1"]
    assert headers == expected_headers, f"manifest.csv headers are incorrect. Expected {expected_headers}, got {headers}"

    data_rows = rows[1:]
    assert len(data_rows) == 4, f"Expected exactly 4 data rows in manifest.csv, found {len(data_rows)}"

    titles = [row[0] for row in data_rows]
    assert titles == sorted(titles), "manifest.csv is not sorted alphabetically by the Title column"

def test_organized_files_exist_and_match_manifest():
    manifest_path = "/home/user/organized_docs/manifest.csv"
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)[1:]

    for title, rel_path, expected_sha1 in rows:
        abs_path = os.path.join("/home/user/organized_docs", rel_path)

        assert os.path.isfile(abs_path), f"File specified in manifest is missing from disk: {abs_path}"

        with open(abs_path, 'rb') as f:
            content = f.read()
            actual_sha1 = hashlib.sha1(content).hexdigest()

        assert actual_sha1 == expected_sha1, f"SHA1 hash mismatch for {abs_path}. Manifest says {expected_sha1}, but file is {actual_sha1}"