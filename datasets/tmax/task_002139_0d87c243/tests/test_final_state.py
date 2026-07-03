# test_final_state.py
import os
import json
import struct
import hashlib
import subprocess
import pytest

def get_text_section_address(elf_path):
    assert os.path.exists(elf_path), f"Evidence file missing: {elf_path}"
    result = subprocess.run(["readelf", "-WS", elf_path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run readelf on evidence.elf"

    for line in result.stdout.split('\n'):
        parts = line.split()
        if len(parts) > 2 and parts[1] == ".text":
            return int(parts[4], 16)
    pytest.fail("Could not find .text section in readelf output")

def test_payload_bin():
    """Verify the payload.bin contains exactly 72 NOPs and the correct Little-Endian address."""
    elf_path = "/home/user/evidence.elf"
    payload_path = "/home/user/payload.bin"

    assert os.path.exists(payload_path), f"Missing payload file: {payload_path}"

    addr_int = get_text_section_address(elf_path)
    expected_payload = b'\x90' * 72 + struct.pack('<Q', addr_int)

    with open(payload_path, 'rb') as f:
        actual_payload = f.read()

    assert actual_payload == expected_payload, "Payload content does not match expected bytes (72 NOPs + 8-byte LE address)"

def test_audit_log_json():
    """Verify the audit_log.json contains the correct text_address and payload_sha256."""
    elf_path = "/home/user/evidence.elf"
    json_path = "/home/user/audit_log.json"

    assert os.path.exists(json_path), f"Missing audit log file: {json_path}"

    addr_int = get_text_section_address(elf_path)
    expected_addr_str = hex(addr_int)

    expected_payload = b'\x90' * 72 + struct.pack('<Q', addr_int)
    expected_hash = hashlib.sha256(expected_payload).hexdigest()

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("audit_log.json is not valid JSON")

    assert "text_address" in data, "Missing 'text_address' key in audit_log.json"
    assert data["text_address"] == expected_addr_str, f"Expected text_address {expected_addr_str}, got {data['text_address']}"

    assert "payload_sha256" in data, "Missing 'payload_sha256' key in audit_log.json"
    assert data["payload_sha256"] == expected_hash, f"Expected payload_sha256 {expected_hash}, got {data['payload_sha256']}"