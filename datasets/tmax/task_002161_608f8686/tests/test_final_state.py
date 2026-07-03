# test_final_state.py
import os
import re
import json
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_format_alert.py"
AGENT_PATH = "/home/user/format_alert.py"
EXTRACTED_ALERTS_PATH = "/home/user/extracted_alerts.txt"

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_ipv4():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_fuzz_inputs(n=1000, seed=42):
    random.seed(seed)
    inputs = []
    levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]

    for _ in range(int(n * 0.7)):
        level = random.choice(levels)
        user = generate_random_string(8)
        action = generate_random_string(10)
        ip = generate_random_ipv4()
        payload = {"user": user, "action": action, "ip": ip, "extra": "data"}
        inputs.append(f"[{level}] {json.dumps(payload)}")

    for _ in range(n - int(n * 0.7)):
        choice = random.randint(1, 4)
        if choice == 1:
            # Malformed JSON
            inputs.append(f"[{random.choice(levels)}] {{\"user\": \"abc\", \"action\": \"def\"")
        elif choice == 2:
            # Missing key
            inputs.append(f"[{random.choice(levels)}] {{\"user\": \"abc\", \"action\": \"def\"}}")
        elif choice == 3:
            # Missing prefix
            payload = {"user": generate_random_string(8), "action": generate_random_string(10), "ip": generate_random_ipv4()}
            inputs.append(json.dumps(payload))
        else:
            # Garbage
            inputs.append(generate_random_string(random.randint(10, 150)))

    random.shuffle(inputs)
    return inputs

def run_script(script_path, input_str):
    result = subprocess.run(
        ["python3", script_path],
        input=input_str,
        text=True,
        capture_output=True
    )
    return result.stdout

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle program missing at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent program missing at {AGENT_PATH}"

    inputs = generate_fuzz_inputs(1000)
    for i, inp in enumerate(inputs):
        oracle_out = run_script(ORACLE_PATH, inp)
        agent_out = run_script(AGENT_PATH, inp)

        assert oracle_out == agent_out, (
            f"Output mismatch on input {i}:\n"
            f"Input: {inp!r}\n"
            f"Oracle output: {oracle_out!r}\n"
            f"Agent output: {agent_out!r}"
        )

def test_extracted_alerts_file():
    assert os.path.isfile(EXTRACTED_ALERTS_PATH), f"Missing extracted alerts file at {EXTRACTED_ALERTS_PATH}"

    with open(EXTRACTED_ALERTS_PATH, "r") as f:
        content = f.read()

    alert_blocks = re.findall(r'ALERT LEVEL: \w+', content)
    assert len(alert_blocks) == 12, f"Expected exactly 12 alert blocks, found {len(alert_blocks)}"

    # Check for blank lines between blocks
    blocks = content.strip().split('\n\n')
    assert len(blocks) == 12, "Expected blank lines separating the 12 alert blocks"