# test_final_state.py
import os
import subprocess
import random
import string
import pytest

AGENT_SCRIPT = "/home/user/sign_request.py"
ORACLE_BINARY = "/app/legacy_signer"

def generate_inputs(n=1000):
    random.seed(42)
    inputs = []

    # 70% valid alphanumeric strings of length 8 to 32
    for _ in range(int(n * 0.7)):
        length = random.randint(8, 32)
        inputs.append("".join(random.choices(string.ascii_letters + string.digits, k=length)))

    # 10% strings shorter than 8 characters
    for _ in range(int(n * 0.1)):
        length = random.randint(1, 7)
        inputs.append("".join(random.choices(string.ascii_letters + string.digits, k=length)))

    # 10% strings longer than 32 characters
    for _ in range(int(n * 0.1)):
        length = random.randint(33, 64)
        inputs.append("".join(random.choices(string.ascii_letters + string.digits, k=length)))

    # 10% strings containing non-alphanumeric characters
    for _ in range(int(n * 0.1)):
        length = random.randint(8, 32)
        s = list("".join(random.choices(string.ascii_letters + string.digits, k=length)))
        s[random.randint(0, length - 1)] = random.choice("!@#$%^&*()_+~`-=[]{}|;':,./<>?")
        inputs.append("".join(s))

    random.shuffle(inputs)
    return inputs

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", -1

def test_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BINARY), "Oracle binary missing"

    inputs = generate_inputs(1000)

    # Add a few edge cases related to arguments
    commands_to_test = [
        ([ORACLE_BINARY], ["python3", AGENT_SCRIPT]),
        ([ORACLE_BINARY, "arg1", "arg2"], ["python3", AGENT_SCRIPT, "arg1", "arg2"])
    ]

    for oracle_cmd, agent_cmd in commands_to_test:
        o_out, o_err, o_code = run_cmd(oracle_cmd)
        a_out, a_err, a_code = run_cmd(agent_cmd)

        assert o_out == a_out, f"Mismatch on stdout for args {oracle_cmd[1:]}. Expected: {repr(o_out)}, Got: {repr(a_out)}"
        assert o_code == a_code, f"Mismatch on return code for args {oracle_cmd[1:]}. Expected: {o_code}, Got: {a_code}"

    # Fuzz inputs
    for inp in inputs:
        oracle_cmd = [ORACLE_BINARY, inp]
        agent_cmd = ["python3", AGENT_SCRIPT, inp]

        o_out, o_err, o_code = run_cmd(oracle_cmd)
        a_out, a_err, a_code = run_cmd(agent_cmd)

        assert o_out == a_out, f"Mismatch on stdout for input {repr(inp)}. Expected: {repr(o_out)}, Got: {repr(a_out)}"
        assert o_code == a_code, f"Mismatch on return code for input {repr(inp)}. Expected: {o_code}, Got: {a_code}"