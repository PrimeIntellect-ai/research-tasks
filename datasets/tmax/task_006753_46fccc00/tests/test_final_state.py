# test_final_state.py
import os
import tarfile
import json
import pytest

CURATED_DIR = "/home/user/curated"
MANIFEST_PATH = os.path.join(CURATED_DIR, "manifest.jsonl")

def test_curated_files_exist():
    # Expected to be curated (author: alice)
    expected_files = ["app_v1.tar", "tool_v3.tar"]
    for f in expected_files:
        path = os.path.join(CURATED_DIR, f)
        assert os.path.isfile(path), f"Expected curated file {path} is missing."

def test_unapproved_files_do_not_exist():
    # Expected NOT to be curated (author: bob, charlie)
    unexpected_files = ["lib_v2.tar", "app_v2.tar", "lib_v2.tar.gz.tar", "app_v2.zip.tar"]
    for f in unexpected_files:
        path = os.path.join(CURATED_DIR, f)
        assert not os.path.exists(path), f"Unapproved artifact was curated: {path}"

def test_tar_contents_app_v1():
    tar_path = os.path.join(CURATED_DIR, "app_v1.tar")
    assert os.path.exists(tar_path), f"File {tar_path} not found."

    with tarfile.open(tar_path, "r") as tar:
        members = tar.getnames()
        # Ensure it contains the expected files
        assert "meta.json" in members or "./meta.json" in members, "meta.json missing in app_v1.tar"
        assert "bin/execute" in members or "./bin/execute" in members, "bin/execute missing in app_v1.tar"

def test_tar_contents_tool_v3():
    tar_path = os.path.join(CURATED_DIR, "tool_v3.tar")
    assert os.path.exists(tar_path), f"File {tar_path} not found."

    with tarfile.open(tar_path, "r") as tar:
        members = tar.getnames()
        # Ensure it contains the expected files
        assert "meta.json" in members or "./meta.json" in members, "meta.json missing in tool_v3.tar"
        assert "src/tool.py" in members or "./src/tool.py" in members, "src/tool.py missing in tool_v3.tar"

def test_manifest_contents():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} is missing."

    with open(MANIFEST_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in manifest.jsonl, found {len(lines)}."

    records = []
    for line in lines:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in manifest.jsonl: {line}")

    expected_records = [
        {"original": "app_v1.zip", "curated": "app_v1.tar", "build": 101},
        {"original": "tool_v3.tar.bz2", "curated": "tool_v3.tar", "build": 103}
    ]

    for expected in expected_records:
        assert expected in records, f"Expected record {expected} missing from manifest.jsonl"