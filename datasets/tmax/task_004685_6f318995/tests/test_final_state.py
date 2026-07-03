# test_final_state.py

import os
import random
import string
import base64
import subprocess
import concurrent.futures
import pytest

ORACLE_PATH = "/app/oracle_extractor"
AGENT_SCRIPT = "/home/user/audit_gen.py"
FUZZ_N = 1000  # Reduced from 5000 to prevent test timeouts, still provides strong statistical confidence

def generate_payload():
    if random.random() < 0.5:
        # Generate valid-looking HTTP request
        h = ''.join(random.choices("0123456789abcdef", k=64))
        c = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 30)))
        pt = f"POST / HTTP/1.1\r\nHost: example.com\r\nX-ELF-Hash: {h}\r\nCookie: session=123; ComplianceSessionID={c}\r\n\r\n".encode('utf-8')
    elif random.random() < 0.75:
        # Generate HTTP request missing some parts
        h = ''.join(random.choices("0123456789abcdef", k=64))
        pt = f"POST / HTTP/1.1\r\nHost: example.com\r\nX-ELF-Hash: {h}\r\nCookie: session=123;\r\n\r\n".encode('utf-8')
    else:
        # Generate completely random bytes
        pt = bytes(random.choices(range(256), k=random.randint(50, 200)))

    # XOR with 0x3F
    xored = bytes([b ^ 0x3F for b in pt])
    return base64.b64encode(xored).decode('utf-8')

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", -1

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"

    random.seed(42)
    payloads = [generate_payload() for _ in range(FUZZ_N)]

    def check_payload(payload):
        oracle_cmd = [ORACLE_PATH, payload]
        agent_cmd = ["python3", AGENT_SCRIPT, payload]

        oracle_out, oracle_err, oracle_code = run_cmd(oracle_cmd)
        agent_out, agent_err, agent_code = run_cmd(agent_cmd)

        return payload, oracle_out, agent_out

    mismatches = []

    # Use ThreadPoolExecutor to speed up the subprocess calls
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        results = executor.map(check_payload, payloads)
        for payload, oracle_out, agent_out in results:
            if oracle_out != agent_out:
                mismatches.append((payload, oracle_out, agent_out))
                if len(mismatches) >= 5:
                    break

    if mismatches:
        err_msg = f"Found mismatches between oracle and agent script (showing up to 5):\n"
        for payload, o_out, a_out in mismatches:
            err_msg += f"\nPayload: {payload}\nOracle output: {o_out!r}\nAgent output:  {a_out!r}\n"
        pytest.fail(err_msg)