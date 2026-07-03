# test_final_state.py
import os
import json
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/legacy_detector"
AGENT_PATH = "/home/user/detector.py"

def generate_random_msg(length=20):
    chars = []
    for _ in range(length):
        choice = random.random()
        if choice < 0.5:
            chars.append(random.choice(string.ascii_letters + string.digits + " !@#$%^&*()"))
        elif choice < 0.7:
            # valid unicode escape
            chars.append(f"\\u{random.randint(0, 0xFFFF):04x}")
        elif choice < 0.9:
            # invalid unicode escape
            bad_hex = "".join(random.choices(string.ascii_letters[6:] + string.digits, k=random.randint(1, 4)))
            chars.append(f"\\u{bad_hex}")
        else:
            # raw unicode
            chars.append(chr(random.randint(0x00A0, 0x02AF)))
    return "".join(chars)

def generate_fuzz_input(num_lines):
    lines = []
    ts = random.randint(0, 1000)
    for _ in range(num_lines):
        ts += random.randint(1, 10)
        obj = {"ts": ts}

        metric_choice = random.random()
        if metric_choice < 0.15:
            if random.random() < 0.5:
                obj["metric"] = None
            # else omit metric
        else:
            obj["metric"] = round(random.uniform(-100.0, 100.0), 4)

        # Add msg, but we must construct the json string manually to preserve the literal \u escapes
        # json.dumps will escape backslashes, so we need to be careful.
        msg_val = generate_random_msg(random.randint(5, 30))

        # We can dump the object without msg, then add msg manually.
        base_json = json.dumps(obj)
        # remove closing brace
        base_json = base_json[:-1]

        # safely encode msg_val: we actually want literal backslashes in the output for the escapes
        # so if msg_val has \uXXXX, we want the JSON to contain \uXXXX literally.
        # json.dumps("\\uXXXX") -> '"\\\\uXXXX"'
        # We want '"\\uXXXX"'
        # So we just construct the string.
        # Wait, if msg_val contains raw unicode, json.dumps will handle it.
        # Let's just build the JSON string directly.

        metric_part = ""
        if "metric" in obj:
            if obj["metric"] is None:
                metric_part = ', "metric": null'
            else:
                metric_part = f', "metric": {obj["metric"]}'

        # For msg, we need to escape quotes and backslashes that are NOT part of our intentional \u escapes.
        # Actually, simpler: generate the string, and just write it.
        # But wait, our generate_random_msg produces a python string like "\\u0041".
        # If we just put it in quotes: f'"msg": "{msg_val}"'
        # We must make sure there are no unescaped quotes in msg_val.
        msg_val = msg_val.replace('"', '\\"')

        line = f'{{"ts": {ts}{metric_part}, "msg": "{msg_val}"}}'
        lines.append(line)

    return "\n".join(lines) + "\n"

@pytest.mark.parametrize("seed", range(100))
def test_fuzz_equivalence(seed):
    random.seed(seed)
    num_lines = random.randint(10, 200)
    input_data = generate_fuzz_input(num_lines)
    input_bytes = input_data.encode('utf-8')

    assert os.path.exists(ORACLE_PATH), "Oracle binary not found."
    assert os.path.exists(AGENT_PATH), "Agent script not found."

    oracle_proc = subprocess.run(
        [ORACLE_PATH],
        input=input_bytes,
        capture_output=True
    )

    agent_proc = subprocess.run(
        ["python3", AGENT_PATH],
        input=input_bytes,
        capture_output=True
    )

    assert agent_proc.returncode == oracle_proc.returncode, (
        f"Return code mismatch. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}\n"
        f"Input:\n{input_data}"
    )

    assert agent_proc.stdout == oracle_proc.stdout, (
        f"Output mismatch on seed {seed}.\n"
        f"Input:\n{input_data}\n"
        f"Oracle output:\n{oracle_proc.stdout.decode('utf-8', errors='replace')}\n"
        f"Agent output:\n{agent_proc.stdout.decode('utf-8', errors='replace')}"
    )