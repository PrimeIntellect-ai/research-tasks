# test_final_state.py
import os
import zlib
import random
import requests
import pytest

def compute_expected_fingerprint(data: bytes) -> str:
    crc = zlib.crc32(data) & 0xFFFFFFFF
    mod = 1000000007
    val = 0
    for b in data:
        val = (val * crc + b) % mod
    return f"{crc:08x}-{val:08x}"

def test_zlib_makefile_fixed():
    makefile_path = "/app/vendored/zlib-1.3.1/Makefile"
    assert os.path.exists(makefile_path), f"Makefile not found at {makefile_path}"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-DBROKEN_SYNTAX_ERROR_INJECTED_BY_CONTRIBUTOR" not in content, (
        "The Makefile still contains the injected broken syntax error flag."
    )

def test_zlib_compiled():
    libz_path = "/app/vendored/zlib-1.3.1/libz.a"
    assert os.path.exists(libz_path), f"Compiled library not found at {libz_path}. Did you compile zlib?"

@pytest.mark.parametrize("payload_size", [0, 5, 1024, 5000])
def test_server_compute_endpoint(payload_size):
    # Generate random binary data
    if payload_size == 0:
        data = b""
    else:
        data = bytes(random.choices(range(256), k=payload_size))

    expected_fingerprint = compute_expected_fingerprint(data)

    url = "http://127.0.0.1:9090/compute"
    try:
        response = requests.post(url, data=data, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    actual_fingerprint = response.text.strip()
    assert actual_fingerprint == expected_fingerprint, (
        f"Fingerprint mismatch for payload of size {payload_size}.\n"
        f"Expected: {expected_fingerprint}\n"
        f"Actual:   {actual_fingerprint}"
    )

def test_server_specific_payloads():
    payloads = [
        b"hello world",
        b"OpenAI",
        b"\x00\x01\x02\x03\x04\x05",
        b"A" * 100
    ]

    url = "http://127.0.0.1:9090/compute"
    for data in payloads:
        expected = compute_expected_fingerprint(data)
        try:
            response = requests.post(url, data=data, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to the server at {url}: {e}")

        assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

        actual = response.text.strip()
        assert actual == expected, (
            f"Fingerprint mismatch for payload {data!r}.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )