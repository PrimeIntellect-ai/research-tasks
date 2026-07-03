# test_final_state.py

import os
import json
import re
import hashlib
import pytest

OUTPUT_FILE = "/home/user/clean_logs.jsonl"

def test_output_file_exists():
    """Verify that the clean_logs.jsonl file was created."""
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a regular file."

def test_output_format_and_deduplication():
    """Verify JSONL format, correct fields, and deduplication by hash."""
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 5, f"Expected exactly 5 unique log lines after deduplication, found {len(lines)}."

    seen_hashes = set()

    for i, line in enumerate(lines):
        if not line.strip():
            continue

        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            pytest.fail(f"Line {i+1} is not valid JSON: {e}\nLine content: {line}")

        for field in ["id", "ip", "message", "msg_hash"]:
            assert field in obj, f"Line {i+1} is missing the '{field}' field."

        seen_hashes.add(obj["msg_hash"])

    assert len(seen_hashes) == 5, "Duplicate messages found in the output. Deduplication failed."

def test_ip_anonymization():
    """Verify that the final octet of all IP addresses is masked with XXX."""
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            obj = json.loads(line)
            ip = obj.get("ip", "")
            assert re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.XXX$", ip), \
                f"IP address '{ip}' on line {i+1} is not masked correctly."

def test_unicode_normalization_and_hashing():
    """Verify that invalid unicode escapes are fixed and msg_hash is correct."""
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Check raw file content to ensure no invalid \uXXXX sequences remain
    # We look for literal \u followed by 4 characters.
    matches = re.findall(r'\\u(.{4})', content)
    for match in matches:
        assert re.match(r'^[0-9a-fA-F]{4}$', match), \
            f"Found invalid unicode escape sequence in raw output: \\u{match}"

    # Verify the computed hashes
    lines = content.strip().split('\n')
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        obj = json.loads(line)
        msg = obj["message"]

        # The hash should be the SHA-256 of the decoded message string
        expected_hash = hashlib.sha256(msg.encode('utf-8')).hexdigest()
        actual_hash = obj["msg_hash"]

        assert actual_hash == expected_hash, \
            f"msg_hash incorrect on line {i+1}.\nExpected: {expected_hash}\nActual: {actual_hash}"