# test_final_state.py

import os
import struct
import subprocess
import tempfile
import pytest

FILE_PATH = "/home/user/evasion.plug"

def test_evasion_plug_exists():
    """Test that the generated payload file exists."""
    assert os.path.isfile(FILE_PATH), f"The file {FILE_PATH} does not exist. Did you run your script?"

def test_evasion_plug_format():
    """Test that the payload file strictly adheres to the custom .plug format."""
    with open(FILE_PATH, "rb") as f:
        data = f.read()

    assert len(data) > 8, "File is too small to contain even the basic headers."

    # 1. Magic Bytes
    assert data[0:4] == b'PLUG', f"Invalid magic bytes. Expected 'PLUG', got {data[0:4]!r}"

    # 2. Certificate Length
    cert_len = struct.unpack('<I', data[4:8])[0]
    assert len(data) >= 8 + cert_len, "File is truncated; smaller than the specified certificate length."

    # 3. Certificate Data
    cert_data = data[8:8+cert_len]

    # Verify the certificate is a valid PEM using OpenSSL (no third-party python libs)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(cert_data)
        tmp_name = tmp.name

    try:
        result = subprocess.run(
            ["openssl", "x509", "-in", tmp_name, "-noout"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Certificate failed to parse as valid X.509 PEM. OpenSSL error: {result.stderr}"
    finally:
        os.remove(tmp_name)

    offset = 8 + cert_len
    assert len(data) >= offset + 2, "File is truncated; missing filename length."

    # 4. Filename Length
    fname_len = struct.unpack('<H', data[offset:offset+2])[0]
    offset += 2

    assert len(data) >= offset + fname_len, "File is truncated; smaller than the specified filename length."

    # 5. Filename
    fname = data[offset:offset+fname_len]
    expected_fname = b'../../../../../../tmp/hacked_plugin'
    assert fname == expected_fname, f"Invalid filename. Expected {expected_fname!r}, got {fname!r}"
    offset += fname_len

    # 6. Payload Data
    payload = data[offset:]
    assert len(payload) >= 4, "Payload is too small to contain ELF magic bytes."
    assert payload[0:4] == b'\x7fELF', f"Missing ELF magic bytes in payload. Got {payload[0:4]!r}"
    assert b'REDTEAM_EVASION_SUCCESS' in payload, "Missing 'REDTEAM_EVASION_SUCCESS' string in the payload data."