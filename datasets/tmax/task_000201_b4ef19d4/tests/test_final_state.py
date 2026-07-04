# test_final_state.py

import os
import subprocess
import random
import pytest

def generate_fuzz_inputs(n=10000, seed=42):
    random.seed(seed)
    inputs = []

    hex_chars = "0123456789ABCDEF"

    for _ in range(n):
        length = random.randint(10, 1000)
        s = ""
        while len(s) < length:
            choice = random.random()
            if choice < 0.7:
                # Valid hex pair
                s += random.choice(hex_chars) + random.choice(hex_chars)
            elif choice < 0.9:
                # Valid RLE
                s += random.choice(hex_chars) + random.choice(hex_chars)
                s += ":" + str(random.randint(1, 255))
            elif choice < 0.95:
                # Invalid RLE (multiplier 0 or > 255)
                s += random.choice(hex_chars) + random.choice(hex_chars)
                s += ":" + str(random.choice([0, random.randint(256, 1000)]))
            elif choice < 0.98:
                # Odd length hex
                s += random.choice(hex_chars)
            else:
                # Invalid char
                s += random.choice("GHIJKLMNOPQRSTUVWXYZ-;")

        # Trim to exact length if needed, though exact length isn't strict, just roughly
        inputs.append(s[:length])

    return inputs

def test_fast_decoder_exists():
    assert os.path.isfile("/home/user/fast_decoder.cpp"), "Source file /home/user/fast_decoder.cpp is missing."
    assert os.path.isfile("/home/user/fast_decoder"), "Compiled binary /home/user/fast_decoder is missing."
    assert os.access("/home/user/fast_decoder", os.X_OK), "Compiled binary /home/user/fast_decoder is not executable."

def test_fuzz_equivalence():
    oracle_path = "/opt/verifier/oracle_decoder"
    agent_path = "/home/user/fast_decoder"

    assert os.path.isfile(oracle_path), "Oracle binary missing."
    assert os.path.isfile(agent_path), "Agent binary missing."

    inputs = generate_fuzz_inputs(n=10000, seed=1337)

    for i, inp in enumerate(inputs):
        oracle_proc = subprocess.run(
            [oracle_path, inp],
            capture_output=True,
            text=True
        )

        agent_proc = subprocess.run(
            [agent_path, inp],
            capture_output=True,
            text=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Exit code mismatch on input {i}: {inp!r}\n"
            f"Oracle: {oracle_proc.returncode}\n"
            f"Agent: {agent_proc.returncode}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on input {i}: {inp!r}\n"
            f"Oracle: {oracle_proc.stdout!r}\n"
            f"Agent: {agent_proc.stdout!r}"
        )