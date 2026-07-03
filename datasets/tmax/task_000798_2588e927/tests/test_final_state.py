# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_evidence_extracted():
    assert os.path.isdir("/home/user/evidence"), "Evidence directory not found"
    assert os.path.isfile("/home/user/evidence/access.log"), "access.log not extracted"
    assert os.path.isfile("/home/user/evidence/oracle_redirect"), "oracle_redirect not extracted"

def test_evil_ips_extracted():
    expected_ips = ["10.0.5.12", "192.168.1.105", "203.0.113.42"]
    evil_ips_path = "/home/user/evil_ips.txt"
    assert os.path.isfile(evil_ips_path), f"{evil_ips_path} not found"

    with open(evil_ips_path, "r") as f:
        ips = [line.strip() for line in f if line.strip()]

    assert ips == expected_ips, f"Expected IPs {expected_ips}, but got {ips}"

def generate_fuzz_inputs(n):
    random.seed(42)
    inputs = []

    def random_string(min_len=1, max_len=20):
        length = random.randint(min_len, max_len)
        return ''.join(random.choices(string.ascii_letters + string.digits + "-._~", k=length))

    for _ in range(n):
        choice = random.random()
        if choice < 0.50:
            # Randomly mutated URLs
            schemes = ["http", "https", "ftp", "", "javascript", "data"]
            scheme = random.choice(schemes)
            netloc = random_string() + ".com" if random.random() > 0.5 else ""
            path = "/" + random_string()
            query = f"a={random_string()}&token={random_string()}" if random.random() > 0.5 else ""
            url = ""
            if scheme:
                url += f"{scheme}://"
            if netloc:
                url += netloc
            url += path
            if query:
                url += f"?{query}"
            inputs.append(url)
        elif choice < 0.70:
            # Protocol-relative URLs
            prefix = random.choice(["//", "/\\", "\\\\", "\\/"])
            domain = random_string() + ".com"
            path = "/" + random_string()
            inputs.append(f"{prefix}{domain}{path}")
        elif choice < 0.90:
            # Valid local paths with query parameters
            path = "/" + random_string()
            query = f"user={random.randint(1, 100)}&token={random_string()}" if random.random() > 0.5 else f"user={random.randint(1,100)}"
            inputs.append(f"{path}?{query}")
        else:
            # Completely random ASCII strings
            length = random.randint(1, 200)
            inputs.append(''.join(random.choices(string.printable, k=length)))

    return inputs

def test_safe_redirect_fuzz_equivalence():
    agent_script = "/home/user/safe_redirect.py"
    oracle_binary = "/verifier/oracle_redirect"

    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.isfile(oracle_binary), f"Oracle binary not found at {oracle_binary}"

    # Use N=1000 to keep test execution time reasonable while still providing strong coverage
    inputs = generate_fuzz_inputs(1000)

    for inp in inputs:
        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_binary, inp],
            capture_output=True,
            text=True
        )
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script, inp],
            capture_output=True,
            text=True
        )
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch for input: {repr(inp)}\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output: {repr(agent_out)}"
        )