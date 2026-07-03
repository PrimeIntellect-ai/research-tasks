# test_final_state.py

import os
import json
import zlib
import hashlib
import pytest

DOCPACK_PATH = "/home/user/release.docpack"
DOCS_DIR = "/home/user/docs_raw"

def test_docpack_exists():
    assert os.path.exists(DOCPACK_PATH), f"The final archive {DOCPACK_PATH} was not found."
    assert os.path.isfile(DOCPACK_PATH), f"{DOCPACK_PATH} should be a file."

def test_no_temp_files():
    temp_file = "/home/user/release.tmp"
    assert not os.path.exists(temp_file), f"Temporary file {temp_file} was left behind."

def test_docpack_content_and_structure():
    assert os.path.exists(DOCPACK_PATH), "Docpack missing."

    with open(DOCPACK_PATH, "rb") as f:
        compressed_data = f.read()

    try:
        decompressed_data = zlib.decompress(compressed_data).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to decompress or decode the archive: {e}")

    try:
        data = json.loads(decompressed_data)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON from the decompressed archive: {e}")

    assert "manifest" in data, "The 'manifest' key is missing from the JSON object."
    assert "files" in data, "The 'files' key is missing from the JSON object."

    assert isinstance(data["manifest"], dict), "'manifest' should be a dictionary."
    assert isinstance(data["files"], dict), "'files' should be a dictionary."

def test_docpack_transformed_files_and_manifest():
    assert os.path.exists(DOCPACK_PATH), "Docpack missing."

    with open(DOCPACK_PATH, "rb") as f:
        data = json.loads(zlib.decompress(f.read()).decode('utf-8'))

    files = data.get("files", {})
    manifest = data.get("manifest", {})

    expected_original_files = ["intro.md", "setup.md", "api.md"]

    for filename in expected_original_files:
        assert filename in files, f"File {filename} is missing from the 'files' object."
        assert filename in manifest, f"File {filename} is missing from the 'manifest' object."

        content = files[filename]

        # Check transformations
        assert "AcmeCorp" not in content, f"'AcmeCorp' was not replaced in {filename}."
        assert "v1.0" not in content, f"'v1.0' was not replaced in {filename}."
        assert "ZenithInc" in content, f"'ZenithInc' was not found in {filename}."
        assert "v2.0" in content, f"'v2.0' was not found in {filename}."

        # Check manifest hash
        expected_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        assert manifest[filename] == expected_hash, f"The manifest hash for {filename} is incorrect."

def test_exact_transformed_content():
    assert os.path.exists(DOCPACK_PATH), "Docpack missing."

    with open(DOCPACK_PATH, "rb") as f:
        data = json.loads(zlib.decompress(f.read()).decode('utf-8'))

    files = data.get("files", {})

    expected_content = {
        "intro.md": "Welcome to ZenithInc API v2.0. This is the intro to ZenithInc.\n",
        "setup.md": "To setup ZenithInc software v2.0, run the installer. ZenithInc rocks.\n",
        "api.md": "ZenithInc v2.0 has 5 endpoints. Contact ZenithInc support.\n"
    }

    for filename, expected_text in expected_content.items():
        if filename in files:
            assert files[filename] == expected_text, f"The transformed content of {filename} does not exactly match expectations."