# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def generate_random_input(seed):
    random.seed(seed)
    length = random.randint(0, 5000)
    chars = string.ascii_letters + string.digits + string.whitespace + string.punctuation

    words = []
    current_len = 0
    while current_len < length:
        if random.random() < 0.3:
            # generate a float
            val = (random.random() - 0.5) * 1000
            word = f"{val:.6f}"
        else:
            # generate random word
            word_len = random.randint(1, 10)
            word = "".join(random.choice(chars) for _ in range(word_len))

        words.append(word)
        current_len += len(word) + 1

    return " ".join(words)[:length]

def test_pipeline_exists():
    assert os.path.isfile("/home/user/pipeline"), "Agent's compiled binary /home/user/pipeline is missing."
    assert os.access("/home/user/pipeline", os.X_OK), "Agent's binary /home/user/pipeline is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_pipeline"
    agent_path = "/home/user/pipeline"

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} is missing."
    assert os.path.isfile(agent_path), f"Agent binary {agent_path} is missing."

    N = 2000
    for i in range(N):
        input_data = generate_random_input(seed=i)

        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            text=True,
            capture_output=True
        )
        agent_proc = subprocess.run(
            [agent_path],
            input=input_data,
            text=True,
            capture_output=True
        )

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on random input {i}.\n"
                f"Input (first 100 chars): {repr(input_data[:100])}...\n"
                f"Oracle output: {repr(oracle_out)}\n"
                f"Agent output : {repr(agent_out)}"
            )