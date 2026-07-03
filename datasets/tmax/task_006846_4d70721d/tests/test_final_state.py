# test_final_state.py

import os
import re

def test_non_elf_file_unmodified():
    filepath = "/home/user/binaries/config.bin"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "rb") as f:
        data = f.read()

    assert not data.startswith(b"\x7fELF"), f"File {filepath} should not be an ELF."
    assert b"555-66-7777" in data, f"Non-ELF file {filepath} was modified; original SSN is missing."
    assert b"***-**-****" not in data, f"Non-ELF file {filepath} was modified; contains redaction string."

def test_elf_file_service_a_redacted():
    filepath = "/home/user/binaries/service_a.bin"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "rb") as f:
        data = f.read()

    assert b"123-45-6789" not in data, f"SSN '123-45-6789' was not redacted in {filepath}."
    assert b"***-**-****" in data, f"Redaction string '***-**-****' not found in {filepath}."
    assert data.count(b"***-**-****") == 1, f"Expected exactly 1 redaction in {filepath}."

def test_elf_file_service_b_redacted():
    filepath = "/home/user/binaries/service_b.bin"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "rb") as f:
        data = f.read()

    assert b"987-65-4321" not in data, f"SSN '987-65-4321' was not redacted in {filepath}."
    assert b"000-00-0000" not in data, f"SSN '000-00-0000' was not redacted in {filepath}."
    assert data.count(b"***-**-****") == 2, f"Expected exactly 2 redactions in {filepath}."

def test_audit_log_correct():
    filepath = "/home/user/audit.log"
    assert os.path.isfile(filepath), f"Audit log file {filepath} is missing."

    with open(filepath, "r") as f:
        log_data = f.read()

    expected_a = "[AUDIT] Processed service_a.bin: redacted 1 secrets."
    expected_b = "[AUDIT] Processed service_b.bin: redacted 2 secrets."

    assert expected_a in log_data, f"Audit log is missing expected entry for service_a.bin. Expected: '{expected_a}'"
    assert expected_b in log_data, f"Audit log is missing expected entry for service_b.bin. Expected: '{expected_b}'"
    assert "config.bin" not in log_data, "Audit log incorrectly contains an entry for config.bin, which is not an ELF file."

def test_headers_conf_csp_enforced():
    filepath = "/home/user/headers.conf"
    assert os.path.isfile(filepath), f"Headers config file {filepath} is missing."

    with open(filepath, "r") as f:
        headers = f.read()

    expected_csp = "Content-Security-Policy: default-src 'self';"
    assert expected_csp in headers, f"CSP header was not appended to {filepath}. Expected to find: '{expected_csp}'"