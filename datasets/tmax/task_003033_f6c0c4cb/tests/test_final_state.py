# test_final_state.py
import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/loc_filter"
AGENT_PATH = "/home/user/solution"

def generate_fuzz_input(seed):
    random.seed(seed)
    target_length = random.randint(1024, 10240)
    out = []
    current_length = 0

    while current_length < target_length:
        id_str = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))
        has_comma = random.random() < 0.9

        text_len = random.randint(10, 100)
        text_chars = []
        for _ in range(text_len):
            r = random.random()
            if r < 0.05:
                text_chars.append('\n')
            elif r < 0.10:
                text_chars.append(
                    ''.join(random.choices(string.ascii_lowercase, k=5)) + '@' +
                    ''.join(random.choices(string.ascii_lowercase, k=5)) + '.com'
                )
            else:
                text_chars.append(random.choice(string.ascii_letters + string.digits + " !#$%&'()*+-./:;<=>?@[\\]^_`{|}~"))

        text_str = ''.join(text_chars)
        line = id_str + (',' if has_comma else '') + text_str + '\n'
        out.append(line)
        current_length += len(line)

    return ''.join(out).encode('utf-8')

def test_agent_solution_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary {AGENT_PATH} does not exist."
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} missing."
    assert os.path.exists(AGENT_PATH), f"Agent binary {AGENT_PATH} missing."

    # Run 1000 fuzz iterations to ensure correctness without taking too much time
    num_iterations = 1000

    for i in range(num_iterations):
        input_data = generate_fuzz_input(i)

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if oracle_proc.stdout != agent_proc.stdout:
            # Decode for readable error message, truncating if necessary
            try:
                input_str = input_data.decode('utf-8')
                oracle_out = oracle_proc.stdout.decode('utf-8')
                agent_out = agent_proc.stdout.decode('utf-8')
            except UnicodeDecodeError:
                input_str = repr(input_data)
                oracle_out = repr(oracle_proc.stdout)
                agent_out = repr(agent_proc.stdout)

            if len(input_str) > 500:
                input_str = input_str[:500] + "... [truncated]"
            if len(oracle_out) > 500:
                oracle_out = oracle_out[:500] + "... [truncated]"
            if len(agent_out) > 500:
                agent_out = agent_out[:500] + "... [truncated]"

            pytest.fail(
                f"Mismatch on fuzz iteration {i} (seed {i}).\n"
                f"Input:\n{input_str}\n\n"
                f"Expected Output (Oracle):\n{oracle_out}\n\n"
                f"Actual Output (Agent):\n{agent_out}"
            )