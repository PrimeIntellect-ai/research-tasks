# test_final_state.py

import os
import hashlib
import re
import pytest

OUTPUT_DIR = "/home/user/output_docs"
DOC_101_PATH = os.path.join(OUTPUT_DIR, "doc_101.txt")
DOC_202_PATH = os.path.join(OUTPUT_DIR, "doc_202.txt")
MANIFEST_PATH = os.path.join(OUTPUT_DIR, "manifest.sha256")
CPP_SOURCE_PATH = "/home/user/doc_parser.cpp"
EXECUTABLE_PATH = "/home/user/doc_parser"

def test_output_directory_exists():
    assert os.path.isdir(OUTPUT_DIR), f"Output directory {OUTPUT_DIR} does not exist."

def test_recovered_documents_content():
    assert os.path.isfile(DOC_101_PATH), f"File {DOC_101_PATH} is missing."
    assert os.path.isfile(DOC_202_PATH), f"File {DOC_202_PATH} is missing."

    expected_doc_101 = (
        "Hello, this is the start of the documentation.\n"
        "It describes the system architecture.\n"
    )
    expected_doc_202 = (
        "Chapter 1: Initial Setup.\n"
        "Run the configure script first.\n"
    )

    with open(DOC_101_PATH, "r", encoding="utf-8") as f:
        content_101 = f.read()
    assert content_101 == expected_doc_101, f"Content of {DOC_101_PATH} is incorrect."

    with open(DOC_202_PATH, "r", encoding="utf-8") as f:
        content_202 = f.read()
    assert content_202 == expected_doc_202, f"Content of {DOC_202_PATH} is incorrect."

def test_manifest_checksums():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} is missing."

    # Compute actual hashes
    def compute_sha256(filepath):
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            sha256.update(f.read())
        return sha256.hexdigest()

    hash_101 = compute_sha256(DOC_101_PATH)
    hash_202 = compute_sha256(DOC_202_PATH)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest_content = f.read()

    # The format should be exactly as sha256sum outputs: [hash]  [filename]
    # The filename in the manifest should be just the basename (or path, but usually basename if run from dir)
    # The instructions say: "[hash]  doc_<DOC_ID>.txt"
    assert f"{hash_101}  doc_101.txt" in manifest_content, f"Manifest is missing correct hash entry for doc_101.txt."
    assert f"{hash_202}  doc_202.txt" in manifest_content, f"Manifest is missing correct hash entry for doc_202.txt."

def test_no_temporary_files():
    assert os.path.isdir(OUTPUT_DIR), f"Output directory {OUTPUT_DIR} does not exist."
    files = os.listdir(OUTPUT_DIR)
    temp_files = [f for f in files if f.startswith(".tmp") or f.endswith(".tmp")]
    assert len(temp_files) == 0, f"Temporary files found in {OUTPUT_DIR}: {temp_files}"

def test_cpp_source_and_executable_exist():
    assert os.path.isfile(CPP_SOURCE_PATH), f"C++ source file {CPP_SOURCE_PATH} is missing."
    assert os.path.isfile(EXECUTABLE_PATH), f"Executable {EXECUTABLE_PATH} is missing."
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"File {EXECUTABLE_PATH} is not executable."

def test_atomic_write_implementation():
    assert os.path.isfile(CPP_SOURCE_PATH), f"C++ source file {CPP_SOURCE_PATH} is missing."
    with open(CPP_SOURCE_PATH, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Check for rename function usage
    has_rename = re.search(r'\brename\s*\(', source_code) is not None
    assert has_rename, f"Could not find 'rename(' or 'std::filesystem::rename(' in {CPP_SOURCE_PATH}. Atomic writes using rename are required."