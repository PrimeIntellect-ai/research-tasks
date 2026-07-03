# test_final_state.py

import os
import json
import struct
import zlib
import pytest

FINAL_DOCZ_PATH = "/home/user/final.docz"
CONFIG_PATH = "/home/user/build_config.json"
SIZE_THRESHOLD = 4500

def test_final_docz_exists_and_size():
    assert os.path.exists(FINAL_DOCZ_PATH), f"Missing file: {FINAL_DOCZ_PATH}"
    assert os.path.isfile(FINAL_DOCZ_PATH), f"Not a file: {FINAL_DOCZ_PATH}"

    size = os.path.getsize(FINAL_DOCZ_PATH)
    assert size <= SIZE_THRESHOLD, f"File size {size} exceeds threshold of {SIZE_THRESHOLD} bytes. Ensure you are compressing the concatenated payload at once with zlib level 9."

def test_final_docz_format_and_content():
    assert os.path.exists(FINAL_DOCZ_PATH), f"Missing file: {FINAL_DOCZ_PATH}"
    assert os.path.exists(CONFIG_PATH), f"Missing config file: {CONFIG_PATH}"

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    expected_logical_paths = set(config.values())

    with open(FINAL_DOCZ_PATH, "rb") as f:
        data = f.read()

    assert len(data) >= 8, "File is too small to contain header."

    magic = data[0:4]
    assert magic == b"DOCZ", f"Invalid magic string: expected b'DOCZ', got {magic}"

    index_size = struct.unpack("<I", data[4:8])[0]
    assert len(data) >= 8 + index_size, "File is too small to contain the JSON index specified by the header."

    json_bytes = data[8:8+index_size]
    try:
        index_str = json_bytes.decode("utf-8")
        index = json.loads(index_str)
    except Exception as e:
        pytest.fail(f"Failed to parse JSON index: {e}")

    assert set(index.keys()) == expected_logical_paths, f"Index keys do not match expected logical paths. Expected {expected_logical_paths}, got {set(index.keys())}"

    compressed_payload = data[8+index_size:]
    try:
        payload = zlib.decompress(compressed_payload)
    except Exception as e:
        pytest.fail(f"Failed to decompress payload: {e}")

    # Verify the offsets and lengths
    for logical_path, (offset, length) in index.items():
        assert offset >= 0, f"Invalid offset for {logical_path}"
        assert length > 0, f"Invalid length for {logical_path}"
        assert offset + length <= len(payload), f"Offset and length for {logical_path} exceed payload size"

        extracted_content = payload[offset:offset+length]
        # Basic check to ensure it's valid text (Markdown)
        try:
            extracted_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail(f"Content for {logical_path} is not valid UTF-8.")