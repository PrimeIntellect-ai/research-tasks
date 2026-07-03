# test_final_state.py

import os
import json
import csv
import tarfile
import pytest

ARTIFACTS_DIR = "/home/user/artifacts"
CSV_PATH = "/home/user/curated_summary.csv"
TAR_PATH = "/home/user/stable_artifacts.tar.gz"
RELEASE_LIST_PATH = "/home/user/release_list.txt"

EXPECTED_META = {
    "alpha": {
        "version": "1.0",
        "expected": {"name": "alpha", "version": "1.0", "status": "stable", "curated_at": 1700000000}
    },
    "beta": {
        "version": "2.1",
        "expected": {"name": "beta", "version": "2.1", "status": "stable"}
    },
    "gamma": {
        "version": "0.9",
        "expected": {"name": "gamma", "version": "0.9", "status": "stable", "curated_at": 1700000000}
    }
}

@pytest.mark.parametrize("pkg_name, pkg_info", EXPECTED_META.items())
def test_meta_json_updated(pkg_name, pkg_info):
    version = pkg_info["version"]
    meta_file = os.path.join(ARTIFACTS_DIR, pkg_name, version, "meta.json")

    assert os.path.isfile(meta_file), f"Metadata file {meta_file} is missing."

    with open(meta_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {meta_file} is not valid JSON.")

    assert data == pkg_info["expected"], f"Metadata in {meta_file} does not match expected final state."

def test_curated_summary_csv():
    assert os.path.isfile(CSV_PATH), f"CSV file {CSV_PATH} is missing."

    with open(CSV_PATH, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"CSV file {CSV_PATH} is empty."
    assert rows[0] == ["name", "version", "status"], f"CSV header is incorrect: {rows[0]}"

    data_rows = sorted(rows[1:])
    expected_rows = sorted([
        ["alpha", "1.0", "stable"],
        ["beta", "2.1", "stable"],
        ["gamma", "0.9", "stable"]
    ])

    assert data_rows == expected_rows, f"CSV data rows do not match expected. Found: {data_rows}"

def test_stable_artifacts_tarball():
    assert os.path.isfile(TAR_PATH), f"Tarball {TAR_PATH} is missing."

    try:
        with tarfile.open(TAR_PATH, "r:gz") as tar:
            members = tar.getnames()
    except tarfile.TarError:
        pytest.fail(f"File {TAR_PATH} is not a valid gzip-compressed tarball.")

    expected_files = {
        "alpha/1.0/bin.dat", "alpha/1.0/meta.json",
        "beta/2.1/bin.dat", "beta/2.1/meta.json",
        "gamma/0.9/bin.dat", "gamma/0.9/meta.json"
    }

    # Filter out directory entries if they exist
    actual_files = {m for m in members if not m.endswith("/") and m in expected_files}

    missing = expected_files - set(members)
    assert not missing, f"Tarball is missing expected files: {missing}"

    # Check that there are no extra files (other than directories)
    extra = {m for m in members if not any(m.startswith(d) for d in ["alpha", "beta", "gamma"])}
    assert not extra, f"Tarball contains unexpected files: {extra}"

def test_release_list_txt():
    assert os.path.isfile(RELEASE_LIST_PATH), f"Release list file {RELEASE_LIST_PATH} is missing."
    assert os.path.isfile(CSV_PATH), f"Cannot verify release list order because {CSV_PATH} is missing."

    with open(CSV_PATH, "r", newline="") as f:
        reader = csv.reader(f)
        csv_rows = list(reader)[1:] # skip header

    expected_lines = [f"Package: {row[0]} v{row[1]}" for row in csv_rows]

    with open(RELEASE_LIST_PATH, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Release list content or order is incorrect. Expected: {expected_lines}, Found: {actual_lines}"