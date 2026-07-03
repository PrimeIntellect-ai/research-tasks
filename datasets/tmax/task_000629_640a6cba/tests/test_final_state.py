# test_final_state.py
import os
import json
import hashlib

def test_parsed_config_json():
    json_path = "/home/user/parsed_config.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"File {json_path} is not valid JSON: {e}"

    expected_data = {
        "Network": {
            "IPAddress": "10.0.5.55",
            "Port": "9090",
            "Gateway": "10.0.5.1",
            "Protocol": "TCP"
        },
        "Security": {
            "EnableSSL": "true",
            "CertPath": "/etc/ssl/certs/legacy.crt",
            "MaxConnections": "50"
        }
    }

    assert data == expected_data, f"JSON content in {json_path} does not match expected output. Got: {data}"

def test_manifest_txt():
    json_path = "/home/user/parsed_config.json"
    manifest_path = "/home/user/manifest.txt"

    assert os.path.isfile(manifest_path), f"File {manifest_path} does not exist."
    assert os.path.isfile(json_path), f"File {json_path} missing, cannot verify manifest."

    with open(json_path, "rb") as f:
        json_bytes = f.read()
    expected_sha256 = hashlib.sha256(json_bytes).hexdigest()

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Manifest should contain exactly 2 lines (TIMESTAMP and SHA256), found {len(lines)}."

    timestamp_line = lines[0]
    sha256_line = lines[1]

    assert timestamp_line.startswith("TIMESTAMP="), "First line of manifest must start with 'TIMESTAMP='."
    assert sha256_line.startswith("SHA256="), "Second line of manifest must start with 'SHA256='."

    timestamp_val = timestamp_line.split("=", 1)[1]
    sha256_val = sha256_line.split("=", 1)[1]

    assert timestamp_val == "1715000000", f"Expected TIMESTAMP=1715000000, got {timestamp_val}"
    assert sha256_val == expected_sha256, f"Expected SHA256={expected_sha256}, got {sha256_val}"