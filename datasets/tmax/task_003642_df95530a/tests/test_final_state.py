# test_final_state.py

import os
import random
import string
import subprocess
import urllib.parse
import tempfile

def generate_fuzz_lines(n=500):
    random.seed(42)
    keywords = ["GANDALF", "VOLDEMORT", "SAURON", "SKYWALKER"]
    lines = []
    for _ in range(n):
        length = random.randint(50, 200)
        decoded_chars = []
        while len(decoded_chars) < length:
            if random.random() < 0.15:
                kw = random.choice(keywords)
                decoded_chars.extend(list(kw))
            else:
                decoded_chars.append(random.choice(string.ascii_letters + string.digits + " "))

        decoded_str = "".join(decoded_chars)[:length]
        # URL encode it. Using quote_plus to include some '+' characters for spaces.
        encoded_str = urllib.parse.quote_plus(decoded_str)
        lines.append(encoded_str)
    return lines

def test_fuzz_equivalence():
    agent_bin = "/home/user/cleaner"
    oracle_bin = "/app/oracle_cleaner"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary is not executable: {agent_bin}"
    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary is not executable: {oracle_bin}"

    dict_content = "GANDALF\nVOLDEMORT\nSAURON\nSKYWALKER\n"
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(dict_content)
        dict_path = f.name

    try:
        lines = generate_fuzz_lines(500)
        input_data = "\n".join(lines) + "\n"

        oracle_proc = subprocess.run([oracle_bin, dict_path], input=input_data, text=True, capture_output=True)
        assert oracle_proc.returncode == 0, f"Oracle failed to run: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run([agent_bin, dict_path], input=input_data, text=True, capture_output=True)
        assert agent_proc.returncode == 0, f"Agent program failed to run or crashed: {agent_proc.stderr}"
        agent_out = agent_proc.stdout

        oracle_lines = oracle_out.splitlines()
        agent_lines = agent_out.splitlines()

        assert len(oracle_lines) == len(agent_lines), f"Output line count mismatch. Expected {len(oracle_lines)}, got {len(agent_lines)}"

        for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
            assert o_line == a_line, (
                f"Mismatch on line {i+1}.\n"
                f"Input:  {lines[i]}\n"
                f"Oracle: {o_line}\n"
                f"Agent:  {a_line}"
            )

    finally:
        if os.path.exists(dict_path):
            os.remove(dict_path)