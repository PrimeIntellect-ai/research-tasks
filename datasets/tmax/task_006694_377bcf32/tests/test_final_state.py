# test_final_state.py

import os
import re
import subprocess
import pytest

BUILDER_SCRIPT = "/home/user/builder.sh"
PAYLOAD_FILE = "/home/user/payload.http"
ELF_FILE = "/home/user/target_auth.elf"
WAF_RULES_FILE = "/home/user/waf_rules.txt"

@pytest.fixture(scope="session", autouse=True)
def run_builder():
    """Run the builder script before tests."""
    assert os.path.exists(BUILDER_SCRIPT), f"{BUILDER_SCRIPT} does not exist."
    assert os.access(BUILDER_SCRIPT, os.X_OK), f"{BUILDER_SCRIPT} is not executable."

    try:
        subprocess.run([BUILDER_SCRIPT], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {BUILDER_SCRIPT} failed:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")

def get_expected_cookie():
    """Extract the expected cookie dynamically from the ELF file."""
    try:
        output = subprocess.check_output(["strings", ELF_FILE]).decode("utf-8", errors="ignore")
        match = re.search(r"(SEC_COOKIE_[a-zA-Z0-9]{16})", output)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

def get_waf_blocked_uas():
    """Extract blocked User-Agents from WAF rules."""
    blocked_uas = []
    if os.path.exists(WAF_RULES_FILE):
        with open(WAF_RULES_FILE, "r") as f:
            for line in f:
                match = re.search(r"Block: User-Agent: \.\*(.*?)\.\*", line)
                if match:
                    blocked_uas.append(match.group(1).lower())
    return blocked_uas

def test_payload_file_exists():
    assert os.path.exists(PAYLOAD_FILE), f"Payload file {PAYLOAD_FILE} was not generated."
    assert os.path.isfile(PAYLOAD_FILE), f"{PAYLOAD_FILE} is not a regular file."

def test_payload_crlf_line_endings():
    with open(PAYLOAD_FILE, "rb") as f:
        content = f.read()

    # Check that there are no standalone \n without \r
    # We replace \r\n with empty string, then check if any \n remain
    content_no_crlf = content.replace(b"\r\n", b"")
    assert b"\n" not in content_no_crlf, "Payload contains LF line endings instead of strict CRLF."

def test_payload_request_line_and_evasion():
    with open(PAYLOAD_FILE, "rb") as f:
        content = f.read().decode("utf-8", errors="ignore")

    lines = content.split("\r\n")
    request_line = lines[0]

    assert request_line.startswith("GET /login?"), "Payload does not start with 'GET /login?'."
    assert "next=" in request_line, "Payload missing 'next' parameter in request line."

    # Check evasion: should not contain http:// or https://
    assert "http://" not in request_line, "Payload triggered WAF rule: contains 'http://'."
    assert "https://" not in request_line, "Payload triggered WAF rule: contains 'https://'."

    # Must point to attacker.com/pwn
    assert "attacker.com/pwn" in request_line, "Payload does not redirect to attacker.com/pwn."

def test_payload_headers():
    with open(PAYLOAD_FILE, "rb") as f:
        content = f.read().decode("utf-8", errors="ignore")

    assert "Host: vulnerable.local\r\n" in content, "Payload missing correct Host header."

    expected_cookie = get_expected_cookie()
    assert expected_cookie is not None, "Could not extract cookie from ELF for verification."

    expected_cookie_header = f"Cookie: {expected_cookie}=admin_bypass\r\n"
    assert expected_cookie_header in content, f"Payload missing correct Cookie header: {expected_cookie_header.strip()}"

def test_payload_user_agent_not_blocked():
    with open(PAYLOAD_FILE, "rb") as f:
        content = f.read().decode("utf-8", errors="ignore")

    ua_match = re.search(r"User-Agent:\s*(.*?)\r\n", content, re.IGNORECASE)
    assert ua_match, "Payload missing User-Agent header."

    ua_value = ua_match.group(1).lower()
    blocked_uas = get_waf_blocked_uas()

    for blocked in blocked_uas:
        assert blocked not in ua_value, f"Payload uses a blocked User-Agent containing '{blocked}'."

def test_payload_trailing_crlf():
    with open(PAYLOAD_FILE, "rb") as f:
        content = f.read()

    assert content.endswith(b"\r\n\r\n"), "Payload does not end with an empty line (trailing CRLF) to signify end of headers."