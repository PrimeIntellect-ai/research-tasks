# test_final_state.py

import os
import stat
import json
import subprocess
import binascii
import re
import pytest

def get_expected_suid():
    bin_dir = "/home/user/evidence/bin"
    suid_binaries = []
    if not os.path.isdir(bin_dir):
        return suid_binaries

    for f in os.listdir(bin_dir):
        path = os.path.join(bin_dir, f)
        if os.path.isfile(path):
            st = os.stat(path)
            if st.st_mode & stat.S_ISUID:
                suid_binaries.append(f)
    return sorted(suid_binaries)

def get_expected_cn():
    cert_path = "/home/user/evidence/attacker.crt"
    if not os.path.isfile(cert_path):
        return "c2.evilcorp.local"

    try:
        out = subprocess.check_output(
            ['openssl', 'x509', '-noout', '-subject', '-in', cert_path], 
            stderr=subprocess.DEVNULL
        ).decode('utf-8')

        # Matches OpenSSL subject output formats for CN
        match = re.search(r'CN\s*=\s*([^,\n]+)', out)
        if match:
            return match.group(1).strip()
    except Exception:
        pass

    return "c2.evilcorp.local"

def get_expected_payload(cn):
    payload_path = "/home/user/evidence/payload.enc"
    if not os.path.isfile(payload_path):
        return ""

    with open(payload_path, 'r') as f:
        hex_data = f.read().strip()

    try:
        enc_bytes = binascii.unhexlify(hex_data)
        key_bytes = cn.encode('utf-8')
        dec_bytes = bytearray()
        for i in range(len(enc_bytes)):
            dec_bytes.append(enc_bytes[i] ^ key_bytes[i % len(key_bytes)])
        return dec_bytes.decode('utf-8')
    except Exception:
        return ""

def test_report_json_exists_and_valid():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"The final report file {report_path} was not found."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    assert isinstance(report, dict), f"The JSON in {report_path} must be an object (dictionary)."

def test_report_contents():
    report_path = "/home/user/report.json"
    if not os.path.isfile(report_path):
        pytest.skip("Report file missing, skipping content check.")

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Report file is not valid JSON, skipping content check.")

    expected_suid = get_expected_suid()
    expected_cn = get_expected_cn()
    expected_payload = get_expected_payload(expected_cn)

    # Check SUID binaries
    assert "suid_binaries" in report, "The key 'suid_binaries' is missing from the JSON report."
    assert isinstance(report["suid_binaries"], list), "'suid_binaries' must be a list."
    assert sorted(report["suid_binaries"]) == expected_suid, (
        f"The 'suid_binaries' list is incorrect. Expected {expected_suid}, but got {report['suid_binaries']}."
    )

    # Check Certificate Common Name
    assert "cert_common_name" in report, "The key 'cert_common_name' is missing from the JSON report."
    assert report["cert_common_name"] == expected_cn, (
        f"The 'cert_common_name' is incorrect. Expected '{expected_cn}', but got '{report['cert_common_name']}'."
    )

    # Check Decoded Payload
    assert "decoded_payload" in report, "The key 'decoded_payload' is missing from the JSON report."
    assert report["decoded_payload"] == expected_payload, (
        f"The 'decoded_payload' is incorrect. Expected '{expected_payload}', but got '{report['decoded_payload']}'."
    )