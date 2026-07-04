# test_final_state.py

import os
import gzip
import json
import pytest

ARCHIVE_PATH = '/home/user/stale_archive.gz'
CONFIG_PATH = '/app/coordinator/config.json'

def test_config_updated():
    """Verify the coordinator config was updated correctly."""
    assert os.path.exists(CONFIG_PATH), f"Config file missing at {CONFIG_PATH}"
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    assert config.get("redis_host") == "127.0.0.1", "redis_host not set to 127.0.0.1"
    assert config.get("redis_port") == 6379, "redis_port not set to 6379"
    assert config.get("storage_url") == "http://127.0.0.1:8080/files/", "storage_url not set correctly"

def test_archive_exists():
    """Verify the archive file was created."""
    assert os.path.exists(ARCHIVE_PATH), f"Archive file missing at {ARCHIVE_PATH}"
    assert os.path.isfile(ARCHIVE_PATH), f"Path {ARCHIVE_PATH} is not a file"

def test_archive_contents_and_size():
    """Verify the archive contents are pre-processed and size is below the threshold."""
    assert os.path.exists(ARCHIVE_PATH), f"Archive file missing at {ARCHIVE_PATH}"

    file_size = os.path.getsize(ARCHIVE_PATH)

    try:
        with gzip.open(ARCHIVE_PATH, 'rb') as f:
            content_bytes = f.read()
    except Exception as e:
        pytest.fail(f"Failed to read {ARCHIVE_PATH} as a gzip file: {e}")

    try:
        content = content_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        pytest.fail(f"Failed to decode archive contents as utf-8: {e}")

    # Ensure pre-processing was done
    assert '\r' not in content, "Carriage returns (\\r) were not stripped from the text files."
    assert '  ' not in content, "Multiple spaces were not replaced with a single space."

    # Ensure files were actually downloaded and concatenated
    assert len(content) >= 500, f"Archive decompressed content is too small ({len(content)} bytes), expected at least 500 bytes."

    # Metric threshold check
    threshold = 4500
    assert file_size < threshold, f"Archive file size {file_size} bytes is not below the threshold of {threshold} bytes. Pre-processing might be incomplete or compression not optimal."