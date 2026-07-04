# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/leaky_encoder"
AGENT_PATH = "/home/user/replicate"

def generate_vocab(size=100):
    vocab = []
    for _ in range(size):
        length = random.randint(3, 10)
        word = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        vocab.append(word)
    return vocab

def generate_input(vocab):
    num_lines = random.randint(5, 50)
    lines = []
    for _ in range(num_lines):
        stage = random.choice(["train", "eval"])
        num_words = random.randint(3, 10)
        words = " ".join(random.choices(vocab, k=num_words))
        lines.append(json.dumps({"stage": stage, "text": words}))
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}. Did you compile it?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable."

    random.seed(42)
    vocab = generate_vocab(100)

    # Run 5000 iterations as requested by the fuzz-equivalence distribution
    for i in range(5000):
        inp = generate_input(vocab)

        oracle_proc = subprocess.run([ORACLE_PATH], input=inp, text=True, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=inp, text=True, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed unexpectedly on input:\n{inp}"
        assert agent_proc.returncode == 0, f"Agent program failed (return code {agent_proc.returncode}) on input:\n{inp}\nStderr:\n{agent_proc.stderr}"

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Mismatch on iteration {i}.\n"
            f"Input:\n{inp}\n"
            f"Oracle output:\n{oracle_proc.stdout}\n"
            f"Agent output:\n{agent_proc.stdout}"
        )