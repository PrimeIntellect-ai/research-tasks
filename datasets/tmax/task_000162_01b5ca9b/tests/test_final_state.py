# test_final_state.py

import os
import random
import string
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/secure_upload.py"
ORACLE_SCRIPT = "/app/oracle_validator.py"
N = 2000
TOKEN_CORRECT = "a9f3b20c8d71"
CERTS_DIR = "/app/fuzz_certs"

def generate_fuzz_inputs():
    random.seed(42)
    inputs = []

    path_chars = list(string.ascii_letters + string.digits) + ['/', '.', '%', '\\']
    traversal_sequences = [
        '../', '..%2f', '%2e%2e/', '/var/uploads/../../etc/passwd', 
        '..\\', '%2e%2e%2f', '.%2e/', '%2e./'
    ]

    for _ in range(N):
        # Generate Token
        if random.random() < 0.2:
            token = TOKEN_CORRECT
        else:
            length = random.randint(1, 20)
            token = "".join(random.choices(string.ascii_letters + string.digits, k=length))

        # Select Cert
        cert_idx = random.randint(0, 99)
        cert = os.path.join(CERTS_DIR, f"cert_{cert_idx}.pem")

        # Generate Path
        if random.random() < 0.5:
            # Heavily weighted to include traversal sequences
            path_len_prefix = random.randint(0, 20)
            path_len_suffix = random.randint(0, 20)
            prefix = "".join(random.choices(path_chars, k=path_len_prefix))
            suffix = "".join(random.choices(path_chars, k=path_len_suffix))
            path = prefix + random.choice(traversal_sequences) + suffix
        else:
            # Normal random path
            path_len = random.randint(1, 100)
            path = "".join(random.choices(path_chars, k=path_len))

        inputs.append((path, token, cert))

    return inputs

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.path.exists(ORACLE_SCRIPT), f"Oracle script missing at {ORACLE_SCRIPT}"

    inputs = generate_fuzz_inputs()

    for path, token, cert in inputs:
        args = ["--path", path, "--token", token, "--cert", cert]

        oracle_cmd = ["python3", ORACLE_SCRIPT] + args
        agent_cmd = ["python3", AGENT_SCRIPT] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert agent_res.returncode == oracle_res.returncode, \
            f"Exit code mismatch!\nInput args: {args}\nOracle code: {oracle_res.returncode}\nAgent code: {agent_res.returncode}\nOracle stdout: {oracle_res.stdout.strip()}\nAgent stdout: {agent_res.stdout.strip()}\nOracle stderr: {oracle_res.stderr.strip()}\nAgent stderr: {agent_res.stderr.strip()}"

        assert agent_res.stdout.strip() == oracle_res.stdout.strip(), \
            f"Stdout mismatch!\nInput args: {args}\nOracle stdout: {oracle_res.stdout.strip()}\nAgent stdout: {agent_res.stdout.strip()}"