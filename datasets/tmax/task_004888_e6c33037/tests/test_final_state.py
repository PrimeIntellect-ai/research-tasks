# test_final_state.py
import os
import random
import string
import subprocess
import base64
import pytest

ORACLE_PATH = "/app/bin/legacy_evaluator"
AGENT_SCRIPT = "/home/user/api_integration/run_api.py"

STANDARD_B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
CUSTOM_B64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

def custom_b64encode(data: bytes) -> str:
    std_b64 = base64.b64encode(data).decode('ascii')
    # Remove padding for simplicity or keep it? The prompt doesn't specify padding, but standard b64 has '='.
    # We will translate the standard characters.
    trans = str.maketrans(STANDARD_B64, CUSTOM_B64)
    return std_b64.translate(trans)

def generate_valid_rpn():
    # Generate a valid RPN expression
    stack_depth = 0
    tokens = []
    num_tokens = random.randint(3, 15)
    for _ in range(num_tokens):
        if stack_depth >= 2 and random.random() < 0.5:
            # Add operator
            op = random.choice(['+', '-', '*', '/'])
            if op == '/':
                # To avoid division by zero safely without evaluating, we might just avoid '/' or ensure the last pushed wasn't 0
                # Just push a safe number before division if needed, or just avoid '/' for simplicity in fuzzing
                op = random.choice(['+', '-', '*'])
            tokens.append(op)
            stack_depth -= 1
        else:
            # Add number
            num = random.randint(-100, 100)
            tokens.append(str(num))
            stack_depth += 1

    # Resolve remaining stack
    while stack_depth > 1:
        op = random.choice(['+', '-', '*'])
        tokens.append(op)
        stack_depth -= 1

    return " ".join(tokens)

def generate_fuzz_inputs(n=1000):
    random.seed(42)
    inputs = []
    for _ in range(n):
        if random.random() < 0.7:
            # Valid RPN encoded
            rpn_str = generate_valid_rpn()
            b64_str = custom_b64encode(rpn_str.encode('ascii'))
            inputs.append(b64_str)
        else:
            # Malformed
            length = random.randint(4, 64)
            if random.random() < 0.5:
                # Random custom b64 chars (might decode to invalid RPN)
                s = "".join(random.choice(CUSTOM_B64 + "=") for _ in range(length))
            else:
                # Random printable ASCII (might contain invalid b64 chars)
                s = "".join(random.choice(string.printable) for _ in range(length))
            inputs.append(s)
    return inputs

def test_run_api_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle not executable"

    inputs = generate_fuzz_inputs(1000)

    for i, inp in enumerate(inputs):
        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH, inp],
                capture_output=True,
                text=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout.strip()
            if not oracle_out and oracle_proc.stderr:
                oracle_out = oracle_proc.stderr.strip()
            oracle_code = oracle_proc.returncode
        except subprocess.TimeoutExpired:
            continue # Skip if oracle hangs (unlikely)

        # Run agent
        try:
            agent_proc = subprocess.run(
                ["python3", AGENT_SCRIPT, inp],
                capture_output=True,
                text=True,
                timeout=2
            )
            agent_out = agent_proc.stdout.strip()
            if not agent_out and agent_proc.stderr:
                agent_out = agent_proc.stderr.strip()
            agent_code = agent_proc.returncode
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input: {inp}")

        assert agent_out == oracle_out, (
            f"Output mismatch on input {i}: {inp!r}\n"
            f"Oracle output: {oracle_out!r}\n"
            f"Agent output:  {agent_out!r}"
        )