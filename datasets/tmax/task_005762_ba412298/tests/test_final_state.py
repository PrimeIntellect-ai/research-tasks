# test_final_state.py

import os
import json
import subprocess
import pytest

APP_DIR = "/home/user/app"
FINDINGS_JSON = "/home/user/findings.json"
GEN_CERT_SH = os.path.join(APP_DIR, "gen_cert.sh")
SERVER_CRT = os.path.join(APP_DIR, "server.crt")
SERVER_KEY = os.path.join(APP_DIR, "server.key")

def test_findings_json_exists_and_valid():
    assert os.path.isfile(FINDINGS_JSON), f"File {FINDINGS_JSON} does not exist."
    with open(FINDINGS_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {FINDINGS_JSON} is not valid JSON.")

    assert "api.php" in data, "Key 'api.php' missing in findings.json"
    assert "auth.py_missing_flags" in data, "Key 'auth.py_missing_flags' missing in findings.json"

def test_findings_content():
    with open(FINDINGS_JSON, "r") as f:
        data = json.load(f)

    cwe = data.get("api.php", "")
    assert cwe.upper() == "CWE-78", f"Expected CWE-78 for api.php, got {cwe}"

    flags = data.get("auth.py_missing_flags", [])
    assert isinstance(flags, list), "auth.py_missing_flags should be a list"

    flags_lower = [str(f).lower() for f in flags]
    assert "httponly" in flags_lower, "Missing 'HttpOnly' flag in findings"
    assert "secure" in flags_lower, "Missing 'Secure' flag in findings"
    assert len(flags) == 2, f"Expected exactly 2 flags, got {len(flags)}"

    # Check if sorted alphabetically (case-insensitive check based on original strings)
    assert flags_lower == sorted(flags_lower), "Flags are not sorted alphabetically"

def test_gen_cert_sh_modified():
    assert os.path.isfile(GEN_CERT_SH), f"File {GEN_CERT_SH} does not exist."
    with open(GEN_CERT_SH, "r") as f:
        content = f.read()

    assert "rsa:2048" in content, "gen_cert.sh does not use rsa:2048"
    assert "sha256" in content or "-sha256" in content, "gen_cert.sh does not use sha256"
    assert "rsa:1024" not in content, "gen_cert.sh still contains rsa:1024"
    assert "-md5" not in content, "gen_cert.sh still contains -md5"

def test_certificates_generated_and_valid():
    assert os.path.isfile(SERVER_CRT), f"Certificate {SERVER_CRT} was not generated."
    assert os.path.isfile(SERVER_KEY), f"Key {SERVER_KEY} was not generated."

    result = subprocess.run(
        ["openssl", "x509", "-text", "-noout", "-in", SERVER_CRT],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to parse server.crt with openssl"

    output = result.stdout.lower()
    assert "sha256" in output, "Certificate signature algorithm does not use sha256"
    assert "2048 bit" in output or "rsa 2048" in output or "public-key: (2048 bit)" in output, "Certificate public key is not 2048 bit"