# test_final_state.py

import os
import zipfile
import tarfile
import pytest

ARTIFACTS_DIR = "/home/user/artifacts"
CURATED_DIR = "/home/user/curated_artifacts"
REPORT_FILE = "/home/user/curation_report.txt"

EXPECTED_FILES = [
    "app1.zip",
    "app2.tar.gz",
    "app3.zip",
    "app4.tar.gz"
]

def get_original_data(filename):
    filepath = os.path.join(ARTIFACTS_DIR, filename)
    if filename.endswith(".zip"):
        with zipfile.ZipFile(filepath, 'r') as zf:
            return zf.read("data.bin")
    elif filename.endswith(".tar.gz"):
        with tarfile.open(filepath, 'r:gz') as tf:
            f = tf.extractfile("data.bin")
            return f.read()
    return b""

def read_curated_file(filename, inner_file):
    filepath = os.path.join(CURATED_DIR, filename)
    if filename.endswith(".zip"):
        with zipfile.ZipFile(filepath, 'r') as zf:
            return zf.read(inner_file)
    elif filename.endswith(".tar.gz"):
        with tarfile.open(filepath, 'r:gz') as tf:
            f = tf.extractfile(inner_file)
            return f.read()
    return b""

def test_curated_directory_exists():
    assert os.path.isdir(CURATED_DIR), f"Directory {CURATED_DIR} does not exist."

@pytest.mark.parametrize("filename", EXPECTED_FILES)
def test_curated_files_exist(filename):
    filepath = os.path.join(CURATED_DIR, filename)
    assert os.path.isfile(filepath), f"Expected curated artifact {filepath} does not exist."

def test_report_content():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist."
    with open(REPORT_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[Modified] app1.zip",
        "[Modified] app2.tar.gz",
        "[Unchanged] app3.zip",
        "[Unchanged] app4.tar.gz"
    ]
    assert lines == expected_lines, f"Report content is incorrect. Expected {expected_lines}, got {lines}"

@pytest.mark.parametrize("filename, expected_status", [
    ("app1.zip", b"STATUS=production"),
    ("app2.tar.gz", b"STATUS=production"),
    ("app3.zip", b"STATUS=development"),
    ("app4.tar.gz", b"STATUS=production")
])
def test_manifest_status(filename, expected_status):
    manifest_content = read_curated_file(filename, "manifest.txt")
    lines = manifest_content.split(b'\n')
    status_line = next((line for line in lines if line.startswith(b"STATUS=")), None)
    assert status_line == expected_status, f"In {filename}, expected {expected_status}, got {status_line}"

@pytest.mark.parametrize("filename", EXPECTED_FILES)
def test_data_bin_unchanged(filename):
    original_data = get_original_data(filename)
    curated_data = read_curated_file(filename, "data.bin")
    assert original_data == curated_data, f"data.bin in {filename} was corrupted or changed."