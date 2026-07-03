# test_final_state.py

import os
import base64
import gzip
import pytest

OUTPUT_FILE = "/home/user/consolidated.b64gz"
SCRIPT_FILE = "/home/user/consolidate_docs.sh"

EXPECTED_HEADERS = [
    "===/home/user/legacy_docs/folderA/file1.txt===",
    "===/home/user/legacy_docs/folderB/file2.txt===",
    "===/home/user/legacy_docs/folderB/subfolder/file3.txt===",
    "===/home/user/legacy_docs/link_file.txt==="
]

def get_decoded_content():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."

    with open(OUTPUT_FILE, 'r') as f:
        b64_content = f.read().strip()

    try:
        gzipped_data = base64.b64decode(b64_content)
    except Exception as e:
        pytest.fail(f"Failed to base64 decode the output file: {e}")

    try:
        uncompressed_data = gzip.decompress(gzipped_data)
    except Exception as e:
        pytest.fail(f"Failed to gzip decompress the decoded data: {e}")

    try:
        text_content = uncompressed_data.decode('utf-8')
    except UnicodeDecodeError as e:
        pytest.fail(f"Uncompressed data is not valid UTF-8: {e}")

    return text_content

def test_script_exists():
    assert os.path.isfile(SCRIPT_FILE), f"Script {SCRIPT_FILE} does not exist."

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."

def test_headers_present():
    text_content = get_decoded_content()

    for header in EXPECTED_HEADERS:
        assert header in text_content, f"Expected header {header} not found in the decoded output."

    # Check that there are no other headers from potentially infinite loops
    header_count = sum(1 for line in text_content.splitlines() if line.startswith("===") and line.endswith("==="))
    assert header_count == 4, f"Expected exactly 4 headers, but found {header_count}."

def test_acmecorp_replaced():
    text_content = get_decoded_content()
    assert "AcmeCorp" not in text_content, "'AcmeCorp' was found in the output. It should have been replaced."

def test_zenithinc_count():
    text_content = get_decoded_content()
    count = text_content.count("ZenithInc")
    assert count == 6, f"Expected 'ZenithInc' to appear exactly 6 times, but found it {count} times."