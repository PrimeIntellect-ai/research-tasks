# test_final_state.py

import os
import json
import random
import subprocess
import string
import pytest

def generate_fuzz_input(num_lines=200):
    lines = []
    ts = 1000
    words_pool = ["hello", "world", "redacted", "test", "data", "rust", "python", "foo", "bar"]
    punctuation = string.punctuation
    for _ in range(num_lines):
        ts += random.randint(1, 10)
        val = random.randint(-1000, 1000)

        # Generate note
        num_words = random.randint(0, 10)
        note_words = []
        for _ in range(num_words):
            word = random.choice(words_pool)
            # Add some punctuation
            if random.random() < 0.3:
                word = random.choice(punctuation) + word + random.choice(punctuation)
            # Add some unicode escapes
            if random.random() < 0.2:
                word += f"\\u{random.randint(0x00E0, 0x00FF):04x}"
            note_words.append(word)

        note = " ".join(note_words)
        lines.append(json.dumps({"ts": ts, "note": note, "val": val}))

    return "\n".join(lines) + "\n"

def test_pipeline_fuzz_equivalence():
    oracle_path = "/app/oracle_pipeline"
    agent_path = "/home/user/pipeline"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)

    for i in range(50):
        fuzz_input = generate_fuzz_input(200)

        oracle_proc = subprocess.run(
            [oracle_path],
            input=fuzz_input,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"

        agent_proc = subprocess.run(
            [agent_path],
            input=fuzz_input,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent failed on input {i}. Error: {agent_proc.stderr}"

        oracle_output = oracle_proc.stdout
        agent_output = agent_proc.stdout

        if oracle_output != agent_output:
            # Find the first differing line
            oracle_lines = oracle_output.splitlines()
            agent_lines = agent_output.splitlines()

            for j, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
                if o_line != a_line:
                    pytest.fail(
                        f"Mismatch on stream {i}, line {j}.\n"
                        f"Input line: {fuzz_input.splitlines()[j]}\n"
                        f"Expected (Oracle): {o_line}\n"
                        f"Got (Agent):       {a_line}"
                    )

            # If lengths differ
            pytest.fail(f"Mismatch on stream {i}: output lengths differ. Oracle: {len(oracle_lines)} lines, Agent: {len(agent_lines)} lines.")