# test_final_state.py

import os
import subprocess
import random
import pytest

def test_crash_frame_correct():
    crash_file = "/home/user/crash_frame.txt"
    assert os.path.exists(crash_file), f"File {crash_file} does not exist."

    with open(crash_file, "r") as f:
        content = f.read().strip()

    assert content == "214", f"Expected crash frame 214, but found '{content}' in {crash_file}."

def test_parser_fuzz_equivalence():
    agent_parser = "/home/user/parser"
    oracle_parser = "/app/oracle_parser"

    assert os.path.exists(agent_parser), f"Agent parser not found at {agent_parser}."
    assert os.access(agent_parser, os.X_OK), f"Agent parser at {agent_parser} is not executable."

    assert os.path.exists(oracle_parser), f"Oracle parser not found at {oracle_parser}."
    assert os.access(oracle_parser, os.X_OK), f"Oracle parser at {oracle_parser} is not executable."

    # Generate fuzz inputs
    random.seed(42)
    charset = ''.join(chr(i) for i in range(32, 127))
    n_inputs = 2500
    min_len = 0
    max_len = 120

    fuzz_inputs = []
    for _ in range(n_inputs):
        length = random.randint(min_len, max_len)
        inp = ''.join(random.choice(charset) for _ in range(length))
        fuzz_inputs.append(inp)

    # Also test some specific edge cases
    fuzz_inputs.extend(["", " ", "\n", "\t", "a" * 120])

    for inp in fuzz_inputs:
        input_bytes = (inp + "\n").encode('utf-8')

        oracle_proc = subprocess.run(
            [oracle_parser],
            input=input_bytes,
            capture_output=True
        )

        agent_proc = subprocess.run(
            [agent_parser],
            input=input_bytes,
            capture_output=True
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch for input: {repr(inp)}\n"
            f"Oracle stdout: {repr(oracle_proc.stdout)}\n"
            f"Agent stdout: {repr(agent_proc.stdout)}"
        )