# test_final_state.py

import os
import re
import pytest

def test_png_extraction():
    # Verify true PNGs were moved and renamed correctly
    assert os.path.isfile("/home/user/assets/images/config.txt.png"), "config.txt.png is missing in assets/images/"
    assert os.path.isfile("/home/user/assets/images/unknown_blob.png"), "unknown_blob.png is missing in assets/images/"

    # Verify they still have the PNG header
    for filepath in ["/home/user/assets/images/config.txt.png", "/home/user/assets/images/unknown_blob.png"]:
        with open(filepath, "rb") as f:
            header = f.read(8)
            assert header == b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A", f"{filepath} does not have a valid PNG header"

    # Verify the fake PNG was NOT moved
    assert os.path.isfile("/home/user/project_dump/image.png"), "image.png should not have been moved from project_dump/"
    assert not os.path.exists("/home/user/assets/images/image.png.png"), "image.png should not have been moved to assets/images/"

def test_log_extraction_and_redaction():
    # Check intermediate file exists
    assert os.path.isfile("/home/user/consolidated_critical.txt"), "consolidated_critical.txt is missing"

    with open("/home/user/consolidated_critical.txt", "r") as f:
        lines = f.read().splitlines()

    # There should be 34 CRITICAL lines (4 from top, 30 from loop)
    assert len(lines) == 34, f"Expected 34 critical lines, found {len(lines)}"

    ipv4_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    for line in lines:
        assert "CRITICAL" in line, f"Line missing 'CRITICAL': {line}"
        assert not ipv4_pattern.search(line), f"IPv4 address not redacted in line: {line}"
        assert "[REDACTED]" in line, f"Line missing '[REDACTED]': {line}"

def test_log_chunking():
    chunk1 = "/home/user/assets/logs/critical_chunk_1.txt"
    chunk2 = "/home/user/assets/logs/critical_chunk_2.txt"
    chunk3 = "/home/user/assets/logs/critical_chunk_3.txt"

    assert os.path.isfile(chunk1), f"{chunk1} is missing"
    assert os.path.isfile(chunk2), f"{chunk2} is missing"
    assert os.path.isfile(chunk3), f"{chunk3} is missing"

    with open(chunk1, "r") as f:
        lines1 = f.read().splitlines()
    assert len(lines1) == 15, f"Expected 15 lines in chunk 1, found {len(lines1)}"

    with open(chunk2, "r") as f:
        lines2 = f.read().splitlines()
    assert len(lines2) == 15, f"Expected 15 lines in chunk 2, found {len(lines2)}"

    with open(chunk3, "r") as f:
        lines3 = f.read().splitlines()
    assert len(lines3) == 4, f"Expected 4 lines in chunk 3, found {len(lines3)}"

    # Verify redaction in chunks as a final check
    ipv4_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    for chunk in [chunk1, chunk2, chunk3]:
        with open(chunk, "r") as f:
            content = f.read()
            assert not ipv4_pattern.search(content), f"IPv4 address found in {chunk}"
            assert "[REDACTED]" in content, f"[REDACTED] missing in {chunk}"