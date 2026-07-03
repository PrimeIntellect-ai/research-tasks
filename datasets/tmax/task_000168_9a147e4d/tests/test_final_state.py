# test_final_state.py

import os
import stat
import json
import re
import ssl
import pytest

def test_suspicious_port_file():
    port_file = "/home/user/incident_report/suspicious_port.txt"
    assert os.path.isfile(port_file), f"File {port_file} does not exist."
    with open(port_file, "r") as f:
        content = f.read().strip()
    assert content == "8427", f"Expected port 8427 in {port_file}, but found '{content}'."

def test_extracted_certificate():
    cert_file = "/home/user/incident_report/extracted_cert.pem"
    assert os.path.isfile(cert_file), f"Certificate file {cert_file} does not exist."

    with open(cert_file, "r") as f:
        cert_data = f.read()

    assert "-----BEGIN CERTIFICATE-----" in cert_data, "Certificate does not contain BEGIN CERTIFICATE block."
    assert "-----END CERTIFICATE-----" in cert_data, "Certificate does not contain END CERTIFICATE block."

def test_file_permissions():
    expected_modes = {
        "/home/user/incident_data/log_a.dat": 0o600,
        "/home/user/incident_data/log_b.dat": 0o600,
        "/home/user/incident_data/log_c.dat": 0o600,
        "/home/user/incident_data/log_d.dat": 0o640,
    }

    for filepath, expected_mode in expected_modes.items():
        assert os.path.isfile(filepath), f"Data file {filepath} is missing."
        st = os.stat(filepath)
        mode = stat.S_IMODE(st.st_mode)
        assert mode == expected_mode, f"Permissions of {filepath} are incorrect. Expected {oct(expected_mode)}, got {oct(mode)}."

def test_secured_files_list():
    secured_list_file = "/home/user/incident_report/secured_files.txt"
    assert os.path.isfile(secured_list_file), f"File {secured_list_file} does not exist."

    with open(secured_list_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["log_a.dat", "log_c.dat"]
    assert lines == expected_lines, f"Expected {expected_lines} in {secured_list_file}, but found {lines}."

def test_script_modifications():
    script_path = "/home/user/scripts/decrypt_data.py"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    # Check if the URL has been updated to port 8427
    assert "8427" in content, "The script does not contain the updated port 8427."

    # Check if verify points to the extracted cert
    assert "verify" in content, "The script does not use the 'verify' parameter in requests.get()."
    assert "/home/user/incident_report/extracted_cert.pem" in content, "The script does not verify against the extracted certificate."
    assert "verify=False" not in content.replace(" ", ""), "The script disabled SSL verification (verify=False), which is disallowed."

def test_decrypted_intel_json():
    json_path = "/home/user/incident_report/decrypted_intel.json"
    assert os.path.isfile(json_path), f"JSON file {json_path} does not exist. Did you run the script successfully?"

    with open(json_path, "r") as f:
        try:
            intel = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    expected_intel = {
        "log_a.dat": "encrypted_payload_alpha_decrypted_with_secret_incident_key_99",
        "log_b.dat": "encrypted_payload_beta_decrypted_with_secret_incident_key_99",
        "log_c.dat": "encrypted_payload_gamma_decrypted_with_secret_incident_key_99",
        "log_d.dat": "encrypted_payload_delta_decrypted_with_secret_incident_key_99"
    }

    assert intel == expected_intel, f"Decrypted intel JSON does not match expected output. Got: {intel}"