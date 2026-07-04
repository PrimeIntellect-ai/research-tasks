# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_part1_make_test_passes():
    """Check that the vendored package is fixed and tests pass."""
    work_dir = "/app/auth-redirect-v1.0.0"
    assert os.path.isdir(work_dir), f"Directory {work_dir} is missing."

    result = subprocess.run(
        ["make", "test"],
        cwd=work_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"'make test' failed in {work_dir}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def generate_fuzz_inputs(n=1000):
    random.seed(42)
    base_domains = ["example.com", "corp.internal", "app.co.uk"]

    schemes = ["https://", "http://", "javascript:", "ftp://", "", "//", "https:/", "https:"]
    subdomains = ["", "app.", "sub.sub.", "not", "evil-"]
    paths = [
        "", "/", "/dashboard", "/login?next=/home", 
        "/../etc/passwd", "/%2e%2e/admin", "/%2E%2E/secret",
        "/valid/path/here", "relative", "/api/v1/data"
    ]

    inputs = []
    for _ in range(n):
        base_domain = random.choice(base_domains)

        # Build a random URL
        scheme = random.choice(schemes)
        sub = random.choice(subdomains)

        # Decide if we use the base domain, a fake one, or no domain
        domain_choice = random.choice([base_domain, "evil.com", base_domain + ".evil.com", "other.com"])
        if sub == "not":
            domain = "not" + base_domain
        else:
            domain = sub + domain_choice

        path = random.choice(paths)

        # Randomly add ports
        port = random.choice(["", ":80", ":443", ":8080", ":evil"])

        # Construct URL
        if scheme in ["https://", "http://", "ftp://", "//"]:
            url = f"{scheme}{domain}{port}{path}"
        else:
            url = f"{scheme}{path}"

        # Sometimes just a pure path
        if random.random() < 0.2:
            url = path

        # Sometimes totally malformed
        if random.random() < 0.05:
            url = "".join(random.choices(string.printable, k=random.randint(5, 20)))

        inputs.append((base_domain, url))

    return inputs

def test_part2_validate_redirect_fuzzing():
    agent_script = "/home/user/validate_redirect"
    oracle_script = "/opt/oracle/validate_redirect_oracle.py"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script is not executable: {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script missing: {oracle_script}"

    inputs = generate_fuzz_inputs(1000)

    for base_domain, url in inputs:
        # Run oracle
        oracle_res = subprocess.run(
            [oracle_script, base_domain, url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        oracle_out = oracle_res.stdout.strip()

        # Run agent
        agent_res = subprocess.run(
            [agent_script, base_domain, url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on input!\n"
            f"Base domain: {base_domain}\n"
            f"URL: {url}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}\n"
            f"Agent STDERR: {agent_res.stderr}"
        )