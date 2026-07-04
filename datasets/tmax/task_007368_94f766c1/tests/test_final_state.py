# test_final_state.py

import os
import hashlib
import pytest

STORAGE_POOL = "/home/user/storage_pool"
MANIFEST_PATH = "/home/user/manifest.txt"
INDEXER_SRC = "/home/user/indexer.cpp"
INDEXER_BIN = "/home/user/indexer"
REPORT_PATH = "/home/user/storage_report.log"

def test_symlink_removed():
    symlink_path = os.path.join(STORAGE_POOL, "projectA", "loop_dir")
    assert not os.path.islink(symlink_path), f"Recursive symlink still exists at {symlink_path}"
    assert not os.path.exists(symlink_path), f"Path {symlink_path} should be completely removed"

def test_files_renamed_and_content_updated():
    cpp_files = []
    for root, dirs, files in os.walk(STORAGE_POOL):
        for f in files:
            assert not f.endswith(".cpp.old_backup"), f"Found unrenamed backup file: {os.path.join(root, f)}"
            if f.endswith(".cpp"):
                cpp_files.append(os.path.join(root, f))

    assert len(cpp_files) == 3, f"Expected 3 .cpp files, found {len(cpp_files)}"

    for cpp_file in cpp_files:
        with open(cpp_file, 'r') as f:
            content = f.read()
            assert "// TODO: STORAGE_QUOTA" not in content, f"Unreplaced string found in {cpp_file}"
            # The original data.cpp.old_backup didn't have the string, so it won't have the new one either.
            if "main.cpp" in cpp_file or "utils.cpp" in cpp_file:
                assert "// QUOTA_CHECKED" in content, f"Expected replacement string missing in {cpp_file}"

def test_manifest_generation():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"

    cpp_files = []
    for root, dirs, files in os.walk(STORAGE_POOL):
        for f in files:
            if f.endswith(".cpp"):
                cpp_files.append(os.path.join(root, f))

    expected_lines = []
    for cpp_file in cpp_files:
        with open(cpp_file, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            expected_lines.append(f"{file_hash}  {cpp_file}")

    expected_lines.sort()

    with open(MANIFEST_PATH, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, "Manifest contents do not match expected hashes, formatting, or sorting"

def test_indexer_fixed_and_compiled():
    assert os.path.isfile(INDEXER_SRC), f"Indexer source missing at {INDEXER_SRC}"
    with open(INDEXER_SRC, 'r') as f:
        content = f.read()
        assert "<sys/file.h>" in content, f"{INDEXER_SRC} does not include <sys/file.h>"

    assert os.path.isfile(INDEXER_BIN), f"Compiled indexer binary missing at {INDEXER_BIN}"
    assert os.access(INDEXER_BIN, os.X_OK), f"Compiled indexer at {INDEXER_BIN} is not executable"

def test_report_generated():
    assert os.path.isfile(REPORT_PATH), f"Report file missing at {REPORT_PATH}"

    cpp_files = []
    for root, dirs, files in os.walk(STORAGE_POOL):
        for f in files:
            if f.endswith(".cpp"):
                cpp_files.append(f)

    expected_content = f"Total verified files: {len(cpp_files)}\n"
    with open(REPORT_PATH, 'r') as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"Report content mismatch. Expected '{expected_content}', got '{actual_content}'"