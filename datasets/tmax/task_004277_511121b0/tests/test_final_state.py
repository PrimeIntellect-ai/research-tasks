# test_final_state.py

import os
import zlib
import codecs
import base64
import requests
import pytest

def crc32_hex(s: str) -> str:
    return f"{zlib.crc32(s.encode('utf-8')) & 0xFFFFFFFF:08x}"

def expected_legacy(v: str, payload: str) -> str:
    crc = crc32_hex(payload)
    rot13 = codecs.encode(payload, 'rot_13')
    hex_str = "".join(f"{ord(c):02x}" for c in rot13)
    sorted_hex = "".join(sorted(hex_str))
    return f"LEGACY_{v}_{crc}_{sorted_hex}"

def expected_modern(v: str, payload: str) -> str:
    crc = crc32_hex(payload)
    b32 = base64.b32encode(payload.encode('utf-8')).decode('utf-8').rstrip('=')
    return f"V_{v}_CRC_{crc}_{b32}"

def make_request(v: str, payload: str) -> str:
    url = "http://127.0.0.1:8080/process"
    try:
        resp = requests.post(url, json={"v": v, "payload": payload}, timeout=3)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}. Response body: {resp.text}"

    # Clean up response in case it's returned as a JSON string
    text = resp.text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    return text

def test_build_and_run_script_exists():
    path = "/home/user/build_and_run.sh"
    assert os.path.exists(path), f"Missing build script at {path}"
    assert os.access(path, os.X_OK), f"Build script at {path} must be executable"

def test_rust_project_exists():
    path = "/home/user/encoder_service/Cargo.toml"
    assert os.path.exists(path), f"Missing Rust project configuration at {path}"

@pytest.mark.parametrize("v,payload", [
    ("1.5.2", "test_data"),
    ("0.9.9", "hello"),
    ("1.9.99", "ComplexPayload123!@#"),
])
def test_legacy_logic(v, payload):
    expected = expected_legacy(v, payload)
    actual = make_request(v, payload)
    assert actual == expected, f"Legacy logic failed for v={v}, payload={payload}. Expected {expected}, got {actual}"

@pytest.mark.parametrize("v,payload", [
    ("2.0.0", "test_data"),
    ("2.1.0", "hello"),
    ("10.0.5", "ComplexPayload123!@#"),
])
def test_modern_logic(v, payload):
    expected = expected_modern(v, payload)
    actual = make_request(v, payload)
    assert actual == expected, f"Modern logic failed for v={v}, payload={payload}. Expected {expected}, got {actual}"