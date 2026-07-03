# test_final_state.py

import os
import random
import string
import subprocess
import base64
import pytest

def python_oracle(input_bytes: bytes) -> bytes:
    """
    Python implementation of the payload_encoder behavior:
    1. Bitwise XOR with repeating key 'G0PH3R'.
    2. Base64 encode.
    3. Reverse the Base64 string.
    """
    key = b"G0PH3R"
    xored = bytearray()
    for i, b in enumerate(input_bytes):
        xored.append(b ^ key[i % len(key)])
    b64 = base64.b64encode(xored)
    return b64[::-1]

def test_evidence_extracted():
    """Test that the evidence archive was extracted to the correct location."""
    evidence_dir = "/home/user/evidence"
    assert os.path.isdir(evidence_dir), f"Evidence directory missing: {evidence_dir}"

    payload_encoder = os.path.join(evidence_dir, "payload_encoder")
    assert os.path.isfile(payload_encoder), f"payload_encoder binary missing from {evidence_dir}"

def test_agent_binary_exists():
    """Test that the agent's Go binary exists and is executable."""
    agent_bin = "/home/user/encoder"
    assert os.path.isfile(agent_bin), f"Agent binary missing: {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary is not executable: {agent_bin}"

def test_fuzz_equivalence():
    """
    Fuzz equivalence test:
    Generate 500 random printable ASCII strings of length 1-1000.
    Run the agent's binary and compare output to the oracle.
    """
    agent_bin = "/home/user/encoder"
    assert os.path.isfile(agent_bin), f"Agent binary missing: {agent_bin}"

    random.seed(1337)
    printable_chars = string.printable

    for i in range(500):
        length = random.randint(1, 1000)
        input_str = "".join(random.choice(printable_chars) for _ in range(length))
        input_bytes = input_str.encode('utf-8')

        expected_output = python_oracle(input_bytes)

        try:
            result = subprocess.run(
                [agent_bin],
                input=input_bytes,
                capture_output=True,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on input length {length}")
        except Exception as e:
            pytest.fail(f"Agent binary execution failed: {e}")

        assert result.returncode == 0, f"Agent binary exited with non-zero code {result.returncode} on input length {length}. Stderr: {result.stderr.decode(errors='replace')}"

        actual_output = result.stdout

        if actual_output != expected_output:
            pytest.fail(
                f"Mismatch on input #{i+1} (length {length}).\n"
                f"Input (repr): {repr(input_str[:50])}...\n"
                f"Expected (repr): {repr(expected_output[:50])}...\n"
                f"Actual (repr): {repr(actual_output[:50])}..."
            )