# test_final_state.py
import os
import glob
import gzip
import re

def test_archive_directory_and_chunks():
    archive_dir = "/home/user/archive"
    assert os.path.isdir(archive_dir), f"Directory missing: {archive_dir}"

    chunks = sorted(glob.glob(os.path.join(archive_dir, "prod_logs.gz.part-*")))
    assert len(chunks) > 0, "No chunked files found in /home/user/archive matching 'prod_logs.gz.part-*'"

    # Check chunk sizes: all but the last should be exactly 51200 bytes (50KB)
    for chunk in chunks[:-1]:
        size = os.path.getsize(chunk)
        assert size == 51200, f"Chunk {chunk} has size {size}, expected 51200 (50KB)"

def test_reconstructed_content():
    archive_dir = "/home/user/archive"
    chunks = sorted(glob.glob(os.path.join(archive_dir, "prod_logs.gz.part-*")))
    assert len(chunks) > 0, "No chunked files found to test content"

    # Concatenate chunks
    compressed_data = bytearray()
    for chunk in chunks:
        with open(chunk, "rb") as f:
            compressed_data.extend(f.read())

    # Decompress
    try:
        decompressed_data = gzip.decompress(compressed_data).decode('utf-8')
    except Exception as e:
        assert False, f"Failed to decompress concatenated chunks: {e}"

    lines = decompressed_data.splitlines()
    assert len(lines) > 0, "Decompressed log data is empty"

    # Verify Dev logs not included
    assert not any("Dev user" in line for line in lines), "Dev logs were incorrectly included in the output"

    # Verify DEBUG lines removed
    assert not any("DEBUG" in line for line in lines), "DEBUG lines were not removed from the output"

    # Verify IP redaction
    ip_pattern = re.compile(r"IP:\s*\d+\.\d+\.\d+\.\d+")
    for line in lines:
        assert not ip_pattern.search(line), f"Unredacted IP found in line: {line}"

    # Verify REDACTED is present where IPs used to be
    assert any("IP: REDACTED" in line for line in lines), "Expected 'IP: REDACTED' not found in logs (redaction failed)"

    # Verify expected content from prod logs is still present
    assert any("INFO Normal operation" in line for line in lines), "Expected prod log content ('INFO Normal operation') missing"
    assert any("Failed to load module" in line for line in lines), "Expected prod log content ('Failed to load module') missing"