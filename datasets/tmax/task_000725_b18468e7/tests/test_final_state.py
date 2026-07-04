# test_final_state.py

import os
import sys
import subprocess
import random
import string
import pytest

def test_custom_b64_installed():
    """Verify that the custom_b64 package was successfully fixed and installed."""
    try:
        import custom_b64
    except ImportError:
        pytest.fail("custom_b64 module is not installed or cannot be imported. Did you fix setup.py and install it?")

    assert hasattr(custom_b64, 'decode'), "custom_b64 does not have the expected 'decode' function."

def test_fuzz_equivalence():
    """Fuzz the agent's script against the oracle to ensure bit-exact output matches."""
    oracle_path = "/app/oracle_checker"
    agent_script = "/home/user/check_permissions.py"

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"

    random.seed(1337)

    try:
        import custom_b64
        has_encode = hasattr(custom_b64, 'encode')
    except:
        has_encode = False

    # Attempt to compute the real certificate fingerprint to generate fully valid inputs
    real_fp = "0" * 64
    try:
        import cryptography.x509
        from cryptography.hazmat.backends import default_backend
        import cryptography.hazmat.primitives.hashes
        with open("/app/server.crt", "rb") as f:
            cert = cryptography.x509.load_pem_x509_certificate(f.read(), default_backend())
            real_fp = cert.fingerprint(cryptography.hazmat.primitives.hashes.SHA256()).hex()
    except Exception:
        pass

    N = 1000
    for i in range(N):
        # Build a random HTTP request
        lines = []
        method = random.choice(['GET', 'POST', 'PUT', 'DELETE'])
        path = random.choice(['/api/v1/data', '/login', '/admin', '/'])
        lines.append(f"{method} {path} HTTP/1.1")
        lines.append("Host: localhost")
        lines.append("User-Agent: FuzzTester/1.0")

        # 80% chance to include the target header
        if random.random() < 0.8:
            if has_encode and random.random() < 0.7:
                # Generate a structurally valid payload
                role = random.choice(["admin", "user", "guest", "superuser"])
                # 50% chance to use the correct fingerprint
                fp = real_fp if random.random() < 0.5 else "".join(random.choices("0123456789abcdef", k=64))
                payload = f"testuser|{role}|{fp}".encode('utf-8')
                try:
                    val = custom_b64.encode(payload)
                    if isinstance(val, bytes):
                        val = val.decode('utf-8')
                except Exception:
                    val = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
            else:
                # Generate completely random or invalid base64
                val = ''.join(random.choices(string.ascii_letters + string.digits + "+/=", k=random.randint(10, 80)))

            # Sometimes mess up the header casing slightly (HTTP headers are case-insensitive, but let's test exact match if required)
            header_name = "X-Secure-Auth" if random.random() < 0.9 else "x-secure-auth"
            lines.append(f"{header_name}: {val}")

        # Add some extra random headers
        for _ in range(random.randint(0, 3)):
            h_name = ''.join(random.choices(string.ascii_letters, k=8))
            h_val = ''.join(random.choices(string.ascii_letters, k=10))
            lines.append(f"X-{h_name}: {h_val}")

        lines.append("")
        lines.append("")

        req = "\r\n".join(lines).encode('utf-8')

        # Run oracle
        proc_oracle = subprocess.run([oracle_path], input=req, capture_output=True)
        oracle_out = proc_oracle.stdout.decode('utf-8', errors='replace').strip()

        # Run agent
        proc_agent = subprocess.run([sys.executable, agent_script], input=req, capture_output=True)
        agent_out = proc_agent.stdout.decode('utf-8', errors='replace').strip()

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on fuzz iteration {i}!\n"
                f"Input Request:\n{req.decode('utf-8', errors='replace')}\n"
                f"Oracle Output: {oracle_out!r}\n"
                f"Agent Output:  {agent_out!r}\n"
                f"Agent Stderr:  {proc_agent.stderr.decode('utf-8', errors='replace')}"
            )