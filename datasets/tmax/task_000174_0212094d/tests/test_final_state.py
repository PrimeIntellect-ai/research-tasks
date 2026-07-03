# test_final_state.py

import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/traffic_oracle"
AGENT_PATH = "/home/user/ids_logic"
NUM_ITERATIONS = 10000

def generate_valid_pins():
    valid_pins = []
    for d1 in range(10):
        for d2 in range(10):
            for d3 in range(10):
                for d4 in range(10):
                    if (d1 * 11 + d2 * 7 + d3 * 3 + d4) % 100 == 42:
                        valid_pins.append(f"{d1}{d2}{d3}{d4}")
    return valid_pins

VALID_PINS = generate_valid_pins()

def generate_random_input():
    choices = [
        "short",
        "invalid_pin_format",
        "invalid_pin_hash",
        "valid_pin_clean",
        "valid_pin_xss",
        "valid_pin_sqli",
        "completely_random"
    ]

    choice = random.choice(choices)

    printable = string.ascii_letters + string.digits + string.punctuation + " "

    if choice == "short":
        length = random.randint(0, 7)
        return "".join(random.choices(printable, k=length))

    elif choice == "invalid_pin_format":
        prefix = "".join(random.choices(string.ascii_letters, k=4))
        length = random.randint(4, 252)
        return prefix + "".join(random.choices(printable, k=length))

    elif choice == "invalid_pin_hash":
        while True:
            prefix = "".join(random.choices(string.digits, k=4))
            if prefix not in VALID_PINS:
                break
        length = random.randint(4, 252)
        return prefix + "".join(random.choices(printable, k=length))

    elif choice == "valid_pin_clean":
        prefix = random.choice(VALID_PINS)
        length = random.randint(4, 252)
        # Avoid accidental XSS/SQLi
        payload = "".join(random.choices(string.ascii_letters, k=length))
        return prefix + payload

    elif choice == "valid_pin_xss":
        prefix = random.choice(VALID_PINS)
        xss = random.choice(["<script>", "javascript:"])
        length = random.randint(4, 252 - len(xss))
        payload = "".join(random.choices(printable, k=length))
        # Insert XSS
        insert_pos = random.randint(0, len(payload))
        payload = payload[:insert_pos] + xss + payload[insert_pos:]
        return prefix + payload

    elif choice == "valid_pin_sqli":
        prefix = random.choice(VALID_PINS)
        sqli = random.choice(["UNION SELECT", "' OR '1'='1"])
        length = random.randint(4, 252 - len(sqli))
        payload = "".join(random.choices(printable, k=length))
        # Insert SQLi
        insert_pos = random.randint(0, len(payload))
        payload = payload[:insert_pos] + sqli + payload[insert_pos:]
        return prefix + payload

    else:
        length = random.randint(0, 256)
        return "".join(random.choices(printable, k=length))

def run_target(executable, arg=None):
    cmd = [executable]
    if arg is not None:
        cmd.append(arg)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"

def test_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Missing executable: {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Path is not a file: {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"File is not executable: {AGENT_PATH}"

def test_fuzz_equivalence():
    random.seed(42)

    # Test argc != 2 (no arguments)
    o_code, o_out, o_err = run_target(ORACLE_PATH)
    a_code, a_out, a_err = run_target(AGENT_PATH)

    assert o_code == a_code, f"Exit code mismatch on no arguments. Oracle: {o_code}, Agent: {a_code}"
    assert o_out == a_out, f"Stdout mismatch on no arguments. Oracle: {o_out!r}, Agent: {a_out!r}"
    assert o_err == a_err, f"Stderr mismatch on no arguments. Oracle: {o_err!r}, Agent: {a_err!r}"

    # Fuzz with arguments
    for i in range(NUM_ITERATIONS):
        test_input = generate_random_input()

        o_code, o_out, o_err = run_target(ORACLE_PATH, test_input)
        a_code, a_out, a_err = run_target(AGENT_PATH, test_input)

        assert o_code == a_code, f"Exit code mismatch on iteration {i}. Input: {test_input!r}\nOracle: {o_code}\nAgent: {a_code}"
        assert o_out == a_out, f"Stdout mismatch on iteration {i}. Input: {test_input!r}\nOracle: {o_out!r}\nAgent: {a_out!r}"
        assert o_err == a_err, f"Stderr mismatch on iteration {i}. Input: {test_input!r}\nOracle: {o_err!r}\nAgent: {a_err!r}"