# test_final_state.py
import base64
import random
import string
import subprocess
import os
import pytest

ORACLE_CODE = """
import sys
import base64
import re
import os
import subprocess

def check_elf():
    try:
        # Simple check for 64-bit ELF magic
        with open('/home/user/server.bin', 'rb') as f:
            header = f.read(5)
            if header[:4] != b'\\x7fELF' or header[4] != 2: # 2 is ELFCLASS64
                return False
        return True
    except:
        return False

def main():
    if not check_elf():
        print("AUDIT FAIL: SERVER BINARY INVALID")
        sys.exit(1)

    if len(sys.argv) < 2:
        return

    b64_input = sys.argv[1]

    try:
        proc = subprocess.run(['base64', '-d'], input=b64_input.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            print("DECODE ERROR")
            sys.exit(0)
        decoded = proc.stdout.decode('utf-8', errors='replace')
    except Exception:
        print("DECODE ERROR")
        sys.exit(0)

    if not decoded.startswith("https://"):
        print("INVALID PROTOCOL")
        sys.exit(0)

    rest = decoded[8:]
    domain = rest.split('/', 1)[0]

    if domain == "auth-secure.internal.corp":
        print(f"SAFE - Content-Security-Policy: default-src 'none'; frame-ancestors https://{domain};")
    else:
        print(f"OPEN REDIRECT ALERT: {domain}")

if __name__ == "__main__":
    main()
"""

@pytest.fixture(scope="session", autouse=True)
def setup_oracle():
    os.makedirs("/verify", exist_ok=True)
    with open("/verify/oracle.py", "w") as f:
        f.write(ORACLE_CODE)

def generate_fuzz_inputs(n=1000):
    random.seed(42)
    inputs = []

    domains = ["auth-secure.internal.corp", "evil.com", "example.org", "sub.auth-secure.internal.corp"]
    protocols = ["https://", "http://", "ftp://", ""]
    paths = ["/login", "/admin", "", "/index.html?redirect=1"]

    for _ in range(n):
        choice = random.randint(1, 6)
        if choice == 1:
            # Valid URLs matching approved domain
            url = f"https://auth-secure.internal.corp{random.choice(paths)}"
            inputs.append(base64.b64encode(url.encode()).decode())
        elif choice == 2:
            # Valid URLs with different domains
            url = f"https://{random.choice(domains[1:])}{random.choice(paths)}"
            inputs.append(base64.b64encode(url.encode()).decode())
        elif choice == 3:
            # URLs missing the path
            url = f"https://{random.choice(domains)}"
            inputs.append(base64.b64encode(url.encode()).decode())
        elif choice == 4:
            # URLs with wrong protocol
            url = f"{random.choice(protocols[1:])}{random.choice(domains)}{random.choice(paths)}"
            inputs.append(base64.b64encode(url.encode()).decode())
        elif choice == 5:
            # Invalid base64 strings
            bad_b64 = "".join(random.choices(string.punctuation, k=random.randint(5, 15)))
            inputs.append(bad_b64)
        elif choice == 6:
            # Empty string or random bytes
            if random.random() < 0.5:
                inputs.append("")
            else:
                rand_bytes = bytes(random.choices(range(256), k=random.randint(1, 20)))
                inputs.append(base64.b64encode(rand_bytes).decode())

    return inputs

def test_fuzz_equivalence():
    script_path = "/home/user/auditor.sh"
    assert os.path.exists(script_path), f"Agent script {script_path} not found."
    assert os.access(script_path, os.X_OK), "Agent script is not executable."

    inputs = generate_fuzz_inputs(1000)

    for inp in inputs:
        # Run oracle
        oracle_proc = subprocess.run(["python3", "/verify/oracle.py", inp], capture_output=True, text=True)
        # Run agent script
        agent_proc = subprocess.run([script_path, inp], capture_output=True, text=True)

        # Compare return code and stdout
        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Return code mismatch on input '{inp}'.\n"
            f"Oracle: {oracle_proc.returncode}\n"
            f"Agent: {agent_proc.returncode}"
        )

        oracle_stdout = oracle_proc.stdout.strip()
        agent_stdout = agent_proc.stdout.strip()

        assert oracle_stdout == agent_stdout, (
            f"Stdout mismatch on input '{inp}'.\n"
            f"Oracle: {oracle_stdout}\n"
            f"Agent: {agent_stdout}"
        )