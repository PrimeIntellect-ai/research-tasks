# test_final_state.py

import os
import json
import subprocess
import pytest

REPORT_PATH = "/home/user/report.json"
ROOT_PATH = "/home/user/extracted_root.pem"
TRAFFIC_CERTS_PATH = "/home/user/traffic_certs.pem"

def test_extracted_root_exists():
    """Test that the extracted_root.pem file exists and is a valid certificate."""
    assert os.path.exists(ROOT_PATH), f"Missing file: {ROOT_PATH}"
    assert os.path.isfile(ROOT_PATH), f"Not a file: {ROOT_PATH}"

    # Verify it's a valid cert by running openssl
    try:
        subprocess.check_output(["openssl", "x509", "-in", ROOT_PATH, "-noout"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"{ROOT_PATH} is not a valid x509 certificate. OpenSSL error: {e.output.decode()}")

def test_report_json_exists_and_valid():
    """Test that report.json exists and is valid JSON."""
    assert os.path.exists(REPORT_PATH), f"Missing file: {REPORT_PATH}"
    assert os.path.isfile(REPORT_PATH), f"Not a file: {REPORT_PATH}"

    with open(REPORT_PATH, "r") as f:
        try:
            json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} does not contain valid JSON.")

def test_report_contents():
    """Test that report.json contains the correct metadata."""
    with open(REPORT_PATH, "r") as f:
        report = json.load(f)

    # Check root_ca_subject
    try:
        real_root_subj = subprocess.check_output(
            ["openssl", "x509", "-in", ROOT_PATH, "-subject", "-noout"]
        ).decode().strip()
    except subprocess.CalledProcessError:
        pytest.fail(f"Could not read subject from {ROOT_PATH}")

    assert "root_ca_subject" in report, "Missing 'root_ca_subject' in report.json"
    assert report["root_ca_subject"] == real_root_subj, f"Mismatch in root_ca_subject. Expected: {real_root_subj}"

    # Check leaf_cn
    real_leaf_cn = "target.evilcorp.local"
    assert "leaf_cn" in report, "Missing 'leaf_cn' in report.json"
    assert report["leaf_cn"] == real_leaf_cn, f"Mismatch in leaf_cn. Expected: {real_leaf_cn}"

    # Check leaf_serial
    try:
        cmd = ["openssl", "x509", "-in", TRAFFIC_CERTS_PATH, "-serial", "-noout"]
        serial_output = subprocess.check_output(cmd).decode().strip()
        real_serial = serial_output.split("=")[1].upper()
    except Exception as e:
        pytest.fail(f"Could not read serial from {TRAFFIC_CERTS_PATH}: {e}")

    assert "leaf_serial" in report, "Missing 'leaf_serial' in report.json"
    assert report["leaf_serial"] == real_serial, f"Mismatch in leaf_serial. Expected: {real_serial}"

    # Check chain_valid
    assert "chain_valid" in report, "Missing 'chain_valid' in report.json"
    assert report["chain_valid"] is True, "chain_valid should be true"