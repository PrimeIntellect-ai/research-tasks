# test_final_state.py
import os
import subprocess
import urllib.request
import ssl
import random
import string
import pytest

def test_nginx_tls_and_proxy():
    """Validates Phase 1: Nginx TLS setup, proxying, and CSP headers."""
    assert os.path.exists("/app/cert.pem"), "/app/cert.pem is missing. TLS certificate was not generated."
    assert os.path.exists("/app/key.pem"), "/app/key.pem is missing. TLS key was not generated."

    # Create an unverified SSL context to accept the self-signed certificate
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://localhost:8443/")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            status = response.getcode()
            headers = response.info()
    except urllib.error.HTTPError as e:
        status = e.code
        headers = e.headers
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx on https://localhost:8443/: {e}")

    assert status == 200, f"Expected HTTP status 200 from Flask via Nginx, got {status}"

    csp_header = headers.get("Content-Security-Policy")
    assert csp_header is not None, "Content-Security-Policy header is missing from the response."
    assert csp_header.strip() == "default-src 'self';", f"Incorrect CSP header value. Expected \"default-src 'self';\", got: {csp_header}"

def test_log_processor_fuzz_equivalence():
    """Validates Phase 3: Fuzz equivalence between the agent's script and the oracle."""
    agent_script = "/home/user/log_processor.py"
    oracle_bin = "/app/log_obfuscator_oracle"

    assert os.path.exists(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.exists(oracle_bin), f"Oracle binary missing: {oracle_bin}"

    # Fixed seed for reproducibility
    random.seed(42)

    for i in range(100):
        length = random.randint(10, 100)
        # Generate random hex string
        hex_input = "".join(random.choices(string.hexdigits.lower(), k=length))

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_bin],
                input=hex_input.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2,
                check=True
            )
            oracle_out = oracle_proc.stdout.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle binary failed unexpectedly on input {hex_input}: {e.stderr.decode('utf-8')}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle binary timed out on input {hex_input}")

        # Run agent script
        try:
            agent_proc = subprocess.run(
                ["/usr/bin/python3", agent_script],
                input=hex_input.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2,
                check=True
            )
            agent_out = agent_proc.stdout.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input {hex_input}.\nStderr: {e.stderr.decode('utf-8')}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input {hex_input}")

        assert agent_out == oracle_out, (
            f"Output mismatch on fuzz iteration {i + 1}.\n"
            f"Input (stdin): {hex_input}\n"
            f"Expected Output (Oracle): {oracle_out}\n"
            f"Actual Output (Agent):    {agent_out}"
        )