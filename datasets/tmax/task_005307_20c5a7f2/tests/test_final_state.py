# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

def test_audit_report():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"Audit report missing at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "Audit report must contain at least two lines."

    cwe_line = lines[0].upper()
    assert "CWE-214" in cwe_line or "CWE-497" in cwe_line, "First line must contain CWE-214 or CWE-497."

    explanation = lines[1].lower()
    assert "proc" in explanation or "cmdline" in explanation or "command-line" in explanation or "command line" in explanation, \
        "Second line must explain the /proc/PID/cmdline leakage vector."

def generate_cert(cert_path):
    cmd = [
        "openssl", "req", "-x509", "-newkey", "rsa:2048",
        "-keyout", "/dev/null", "-out", cert_path,
        "-days", "1", "-nodes", "-subj", "/CN=fuzz_test"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def test_payload_encoder_fuzz_equivalence():
    agent_bin = "/home/user/payload_encoder"
    oracle_bin = "/app/obfuscator_bin"

    assert os.path.isfile(agent_bin), f"Agent binary missing at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary is not executable at {agent_bin}"
    assert os.path.isfile(oracle_bin), f"Oracle binary missing at {oracle_bin}"

    random.seed(42)
    charset = string.ascii_letters + string.digits

    # To keep test times reasonable while still providing rigorous fuzzing,
    # we generate a smaller number of certificates and test multiple payloads per cert.
    num_certs = 10
    payloads_per_cert = 1000

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(num_certs):
            cert_path = os.path.join(tmpdir, f"cert_{i}.pem")
            generate_cert(cert_path)

            for _ in range(payloads_per_cert):
                length = random.randint(1, 1024)
                payload = "".join(random.choices(charset, k=length))

                # Run Oracle
                oracle_proc = subprocess.run(
                    [oracle_bin, cert_path, payload],
                    capture_output=True, text=True
                )

                # Run Agent
                agent_proc = subprocess.run(
                    [agent_bin, cert_path, payload],
                    capture_output=True, text=True
                )

                assert oracle_proc.returncode == agent_proc.returncode, \
                    f"Exit code mismatch. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode} for payload len {length}"

                assert oracle_proc.stdout == agent_proc.stdout, \
                    f"Output mismatch for payload: {payload[:20]}... (len {length}).\nOracle: {oracle_proc.stdout}\nAgent: {agent_proc.stdout}"