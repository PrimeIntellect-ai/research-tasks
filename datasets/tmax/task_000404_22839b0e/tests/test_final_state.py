# test_final_state.py

import os
import subprocess
import random
import string
import zipfile
import re
import pytest

def generate_random_string():
    length = random.randint(10, 500)
    chars = string.ascii_letters + string.digits + " -<>"
    s = "".join(random.choice(chars) for _ in range(length))

    # Inject specific patterns to ensure they are tested
    if random.random() < 0.5:
        s += "<script>alert(1)</script>"
    if random.random() < 0.5:
        s += "<img>"
    if random.random() < 0.5:
        # SSN
        s += f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"
    if random.random() < 0.5:
        # CC 16 digits
        s += f"{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
    if random.random() < 0.5:
        # CC 13 digits
        s += f"{random.randint(1000000000000,9999999999999)}"

    # Shuffle the string to mix injected patterns
    s_list = list(s)
    random.shuffle(s_list)
    return "".join(s_list)

def test_fuzz_equivalence():
    agent_script = "/home/user/redact_logs.py"
    oracle_script = "/app/reference_redactor.py"

    assert os.path.exists(agent_script), f"Agent script {agent_script} not found."
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable."

    random.seed(42)
    for _ in range(1000):
        test_input = generate_random_string()

        agent_proc = subprocess.run([agent_script, test_input], capture_output=True, text=True)
        oracle_proc = subprocess.run(["python3", oracle_script, test_input], capture_output=True, text=True)

        assert agent_proc.returncode == 0, f"Agent script failed with error: {agent_proc.stderr}"
        assert agent_proc.stdout == oracle_proc.stdout, f"Mismatch on input: {test_input!r}\nExpected: {oracle_proc.stdout!r}\nGot: {agent_proc.stdout!r}"

def test_block_ips_script():
    script_path = "/home/user/block_ips.sh"
    assert os.path.exists(script_path), f"Missing {script_path}"

    zip_path = "/app/network_logs.zip"
    assert os.path.exists(zip_path), f"Missing {zip_path}"

    try:
        with zipfile.ZipFile(zip_path) as zf:
            log_data = zf.read("access.log", pwd=b"h4ckk3y!").decode("utf-8")
    except Exception as e:
        pytest.fail(f"Could not read access.log from zip using the expected password: {e}")

    sqli_ips = set()
    for line in log_data.splitlines():
        if "UNION SELECT" in line or "OR 1=1" in line:
            match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
            if match:
                sqli_ips.add(match.group(0))

    with open(script_path, "r") as f:
        script_content = f.read()

    for ip in sqli_ips:
        assert f"-s {ip}" in script_content, f"IP {ip} is missing from the iptables rules in {script_path}"
        assert "DROP" in script_content, f"DROP action is missing in {script_path}"