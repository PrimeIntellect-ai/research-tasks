# test_final_state.py

import os
import subprocess
import time
import json
import random
import pytest

# Paths
START_SCRIPT = "/app/start_services.sh"
ORACLE_BIN = "/app/payload_obfuscator"
AGENT_SCRIPT = "/home/user/reconstructed_hasher.py"
REVOKED_SERIAL_FILE = "/home/user/revoked_serial.txt"
CWE_FILE = "/home/user/cwe.txt"
CRL_FILE = "/app/certs/malware_crl.pem"

def test_part1_services_end_to_end():
    """Verify that the multi-service stack is correctly configured and working."""
    # Start the services
    start_proc = subprocess.Popen([START_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)  # Give services time to start

    try:
        # Send a POST request to Nginx
        payload = json.dumps({"data": "verify_test_123"})
        curl_cmd = [
            "curl", "-k", "-s", "-o", "/dev/null", "-w", "%{http_code}",
            "-X", "POST", "https://127.0.0.1:8443/log",
            "-H", "Content-Type: application/json",
            "-d", payload
        ]
        result = subprocess.run(curl_cmd, capture_output=True, text=True)

        # Check if we got a successful HTTP response (e.g., 200 or 201)
        assert result.stdout.strip() in ["200", "201"], f"Expected HTTP 200/201 from Nginx, got {result.stdout.strip()}"

        # Verify the data was stored in Redis
        # We assume redis-cli is available
        redis_cmd = ["redis-cli", "-a", "supersecret", "keys", "*"]
        redis_res = subprocess.run(redis_cmd, capture_output=True, text=True)

        # Checking if 'verify_test_123' or something similar is in Redis
        assert "verify_test_123" in redis_res.stdout or "log" in redis_res.stdout, "Data was not found in Redis after POST request."
    finally:
        # Cleanup: kill started processes if needed, though usually the container is ephemeral
        subprocess.run(["pkill", "-f", "nginx|flask|redis"], capture_output=True)

def test_part2_fuzz_equivalence():
    """Verify that the reconstructed hasher perfectly matches the oracle binary."""
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script missing: {AGENT_SCRIPT}"
    assert os.path.isfile(ORACLE_BIN), f"Oracle binary missing: {ORACLE_BIN}"

    random.seed(42)

    for i in range(100):
        length = random.randint(1, 4096)
        input_data = bytes(random.getrandbits(8) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run([ORACLE_BIN], input=input_data, capture_output=True)
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(["python3", AGENT_SCRIPT], input=input_data, capture_output=True)
        agent_out = agent_proc.stdout

        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i} with input length {length}.\n"
            f"Oracle output length: {len(oracle_out)}\n"
            f"Agent output length: {len(agent_out)}"
        )

def test_part3_cwe_identification():
    """Verify that the correct CWE ID is identified."""
    assert os.path.isfile(CWE_FILE), f"CWE file missing: {CWE_FILE}"
    with open(CWE_FILE, "r") as f:
        cwe_content = f.read().strip()

    assert cwe_content == "CWE-295", f"Incorrect CWE identified. Expected CWE-295, got {cwe_content}"

def test_part3_revoked_serial():
    """Verify that the revoked serial number is correctly identified."""
    assert os.path.isfile(REVOKED_SERIAL_FILE), f"Revoked serial file missing: {REVOKED_SERIAL_FILE}"

    # Extract revoked serial from the CRL using openssl
    openssl_cmd = ["openssl", "crl", "-inform", "PEM", "-text", "-noout", "-in", CRL_FILE]
    result = subprocess.run(openssl_cmd, capture_output=True, text=True)

    # Parse the openssl output for the Serial Number
    # Output looks like:
    # Revoked Certificates:
    #     Serial Number: 7F8A9B12
    #         Revocation Date: ...
    revoked_serial = None
    for line in result.stdout.splitlines():
        if "Serial Number:" in line:
            revoked_serial = line.split("Serial Number:")[1].strip()
            break

    assert revoked_serial is not None, "Could not extract revoked serial from CRL for validation."

    with open(REVOKED_SERIAL_FILE, "r") as f:
        student_serial = f.read().strip().upper()

    assert student_serial == revoked_serial.upper(), f"Incorrect revoked serial. Expected {revoked_serial.upper()}, got {student_serial}"