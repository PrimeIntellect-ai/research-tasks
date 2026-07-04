# test_final_state.py

import os
import pytest

def test_cwe_identification():
    cwe_path = "/home/user/evidence/cwe.txt"
    assert os.path.isfile(cwe_path), f"Missing evidence file: {cwe_path}"

    with open(cwe_path, "r") as f:
        cwe_content = f.read().strip()

    valid_cwes = {"CWE-121", "CWE-120"}
    assert cwe_content in valid_cwes, f"Expected {cwe_path} to contain CWE-121 or CWE-120, but found '{cwe_content}'"

def test_c2_domain():
    c2_path = "/home/user/evidence/c2_domain.txt"
    assert os.path.isfile(c2_path), f"Missing evidence file: {c2_path}"

    with open(c2_path, "r") as f:
        c2_content = f.read().strip()

    expected_domain = "c2-alpha.malicious.local"
    assert c2_content == expected_domain, f"Expected C2 domain to be '{expected_domain}', but found '{c2_content}'"

def test_implant_decoded():
    implant_path = "/home/user/evidence/implant.bin"
    assert os.path.isfile(implant_path), f"Missing decoded implant file: {implant_path}"

    with open(implant_path, "rb") as f:
        implant_data = f.read()

    assert b"SIG_DEADC0DE" in implant_data, "The decoded implant.bin does not contain the expected signature 'SIG_DEADC0DE'. Decoding/Decryption may have failed."

def test_yara_rule_exists_and_looks_valid():
    yar_path = "/home/user/evidence/implant.yar"
    assert os.path.isfile(yar_path), f"Missing YARA rule file: {yar_path}"

    with open(yar_path, "r") as f:
        yar_content = f.read()

    assert "rule " in yar_content, "The file implant.yar does not appear to contain a valid YARA rule structure (missing 'rule' keyword)."
    assert "SIG_DEADC0DE" in yar_content, "The YARA rule does not contain the expected signature string 'SIG_DEADC0DE'."

def test_infected_files_list():
    infected_path = "/home/user/evidence/infected.txt"
    assert os.path.isfile(infected_path), f"Missing infected files list: {infected_path}"

    with open(infected_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_files = {
        "/home/user/forensics/system_files/crond_helper",
        "/home/user/forensics/system_files/sshd_monitor"
    }

    actual_files = set(lines)

    missing = expected_files - actual_files
    extra = actual_files - expected_files

    assert not missing, f"Missing expected infected files in {infected_path}: {missing}"
    assert not extra, f"Found extra (incorrect) files in {infected_path}: {extra}"
    assert len(lines) == 2, f"Expected exactly 2 infected files, but found {len(lines)}"