# test_final_state.py
import os
import stat
import subprocess
import base64
import re

KEYS_DIR = "/home/user/app/keys"
CA_CRT = os.path.join(KEYS_DIR, "ca.crt")
SERVER_CRT = os.path.join(KEYS_DIR, "server.crt")
SERVER_KEY = os.path.join(KEYS_DIR, "server.key")
VALIDATE_SCRIPT = "/home/user/app/validate_jwt.py"
FIREWALL_SCRIPT = "/home/user/app/firewall.sh"

def test_keys_and_permissions():
    """Check that keys exist and server.key has 400 permissions."""
    assert os.path.exists(CA_CRT), f"Missing {CA_CRT}"
    assert os.path.exists(SERVER_CRT), f"Missing {SERVER_CRT}"
    assert os.path.exists(SERVER_KEY), f"Missing {SERVER_KEY}"

    st = os.stat(SERVER_KEY)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Permissions of {SERVER_KEY} are {oct(perms)}, expected 0o400"

def test_certificate_chain():
    """Verify that server.crt is signed by ca.crt."""
    cmd = ["openssl", "verify", "-CAfile", CA_CRT, SERVER_CRT]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Certificate verification failed: {result.stderr}"
    assert "OK" in result.stdout, "Certificate verification output does not contain 'OK'"

def _run_validate_script(token: str) -> str:
    cmd = ["python3", VALIDATE_SCRIPT]
    result = subprocess.run(cmd, input=token, capture_output=True, text=True)
    return result.stdout.strip()

def test_jwt_validation_none_alg():
    """Test that validate_jwt.py rejects an alg=none token."""
    header = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode().rstrip('=')
    payload = base64.urlsafe_b64encode(b'{"sub":"test"}').decode().rstrip('=')
    token = f"{header}.{payload}."

    output = _run_validate_script(token)
    assert output == "INVALID", f"Expected INVALID for none alg token, got {output}"

def test_jwt_validation_valid_rs256():
    """Test that validate_jwt.py accepts a valid RS256 token."""
    header = base64.urlsafe_b64encode(b'{"alg":"RS256","typ":"JWT"}').decode().rstrip('=')
    payload = base64.urlsafe_b64encode(b'{"sub":"test"}').decode().rstrip('=')
    msg = f"{header}.{payload}"

    # Sign using openssl to avoid third-party dependencies in the test
    cmd = ["openssl", "dgst", "-sha256", "-sign", SERVER_KEY]
    result = subprocess.run(cmd, input=msg.encode(), capture_output=True)
    assert result.returncode == 0, "Failed to sign test token"

    sig = base64.urlsafe_b64encode(result.stdout).decode().rstrip('=')
    token = f"{msg}.{sig}"

    output = _run_validate_script(token)
    assert output == "VALID", f"Expected VALID for correctly signed RS256 token, got {output}"

def test_firewall_script():
    """Verify the firewall script contains the required iptables rules."""
    assert os.path.exists(FIREWALL_SCRIPT), f"Missing {FIREWALL_SCRIPT}"
    with open(FIREWALL_SCRIPT, "r") as f:
        content = f.read()

    # Check for ACCEPT rule
    assert re.search(r"iptables\s+-A\s+INPUT\s+.*-p\s+tcp\s+.*-s\s+127\.0\.0\.1\s+.*--dport\s+8000\s+.*-j\s+ACCEPT", content) or \
           re.search(r"iptables\s+-A\s+INPUT\s+.*-s\s+127\.0\.0\.1\s+.*-p\s+tcp\s+.*--dport\s+8000\s+.*-j\s+ACCEPT", content), \
           "Firewall script missing correct ACCEPT rule for 127.0.0.1 on port 8000"

    # Check for DROP rule
    assert re.search(r"iptables\s+-A\s+INPUT\s+.*-p\s+tcp\s+.*--dport\s+8000\s+.*-j\s+DROP", content), \
           "Firewall script missing correct DROP rule for port 8000"