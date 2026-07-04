# test_final_state.py

import os
import time
import struct
import subprocess
import pytest

INCOMING_DIR = "/home/user/incoming_docs"
ARCHIVE_DIR = "/home/user/archive"
ARCHIVE_FILE = os.path.join(ARCHIVE_DIR, "docs.bin")
TEST_FILE = os.path.join(INCOMING_DIR, "eval_drop.txt")

def test_daemon_running():
    """Verify that the doc_watcher daemon is running."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "doc_watcher"]).decode('utf-8')
        assert output.strip(), "doc_watcher process is not running."
    except subprocess.CalledProcessError:
        pytest.fail("doc_watcher process is not running.")

def test_daemon_processing():
    """Drop a test file, wait, and verify the binary archive."""
    # Ensure directories exist
    assert os.path.isdir(INCOMING_DIR), f"{INCOMING_DIR} does not exist."
    assert os.path.isdir(ARCHIVE_DIR), f"{ARCHIVE_DIR} does not exist."

    # Create the ISO-8859-1 test file
    title = "El Niño"
    content = "The weather phenomenon.\n"
    iso_content = (title + "\n" + content).encode('iso-8859-1')

    with open(TEST_FILE, "wb") as f:
        f.write(iso_content)

    # Wait for the daemon to process the file
    time.sleep(3)

    # Verify the test file was deleted
    assert not os.path.exists(TEST_FILE), f"Test file {TEST_FILE} was not deleted by the daemon."

    # Verify the archive file exists
    assert os.path.isfile(ARCHIVE_FILE), f"Archive file {ARCHIVE_FILE} does not exist."

    # Read and parse the archive file
    with open(ARCHIVE_FILE, "rb") as f:
        data = f.read()

    assert len(data) > 0, "Archive file is empty."

    # Parse records to find the last one
    offset = 0
    records = []

    while offset < len(data):
        # Read Magic
        assert offset + 2 <= len(data), "Truncated record (magic bytes)."
        magic = data[offset:offset+2]
        assert magic == b'\xca\xd0', f"Invalid magic bytes at offset {offset}: {magic.hex()}"
        offset += 2

        # Read Title Length
        assert offset + 4 <= len(data), "Truncated record (title length)."
        title_len = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4

        # Read Title
        assert offset + title_len <= len(data), "Truncated record (title)."
        record_title = data[offset:offset+title_len]
        offset += title_len

        # Read Content Length
        assert offset + 4 <= len(data), "Truncated record (content length)."
        content_len = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4

        # Read Content
        assert offset + content_len <= len(data), "Truncated record (content)."
        record_content = data[offset:offset+content_len]
        offset += content_len

        records.append({
            'title': record_title,
            'content': record_content
        })

    assert len(records) > 0, "No records found in archive."

    last_record = records[-1]
    expected_title_utf8 = title.encode('utf-8')
    expected_content_utf8 = content.encode('utf-8')

    assert last_record['title'] == expected_title_utf8, f"Expected title {expected_title_utf8.hex()}, got {last_record['title'].hex()}"
    assert last_record['content'] == expected_content_utf8, f"Expected content {expected_content_utf8.hex()}, got {last_record['content'].hex()}"