# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_panic_code_extracted():
    """Check if the panic code was correctly extracted from the video."""
    panic_code_path = "/home/user/panic_code.txt"
    assert os.path.isfile(panic_code_path), f"File {panic_code_path} is missing."

    with open(panic_code_path, "r") as f:
        content = f.read().strip()

    assert content == "0x8BADF00D", f"Expected panic code '0x8BADF00D', but got '{content}'"

def test_log_parser_compiled_and_executable():
    """Check if the log parser was compiled to the correct location."""
    compiled_parser_path = "/home/user/log_parser"
    assert os.path.isfile(compiled_parser_path), f"Compiled binary {compiled_parser_path} is missing."
    assert os.access(compiled_parser_path, os.X_OK), f"File {compiled_parser_path} is not executable."

def generate_fuzz_lines(n=10000):
    """Generate random log lines for fuzzing."""
    random.seed(42)
    lines = []

    chars = string.ascii_letters + string.digits + " !@#$%^&*()_+-=[]{}|;':\",./<>?"

    for _ in range(n):
        choice = random.random()
        if choice < 0.2:
            # Valid-looking line
            ts = "".join(random.choices(chars.replace("]", ""), k=random.randint(1, 20)))
            lvl = "".join(random.choices(chars.replace(":", ""), k=random.randint(1, 10)))
            msg = "".join(random.choices(chars, k=random.randint(1, 100)))
            lines.append(f"[{ts}] {lvl}: {msg}")
        elif choice < 0.4:
            # Missing ']'
            ts = "".join(random.choices(chars.replace("]", ""), k=random.randint(1, 20)))
            lvl = "".join(random.choices(chars.replace(":", ""), k=random.randint(1, 10)))
            msg = "".join(random.choices(chars, k=random.randint(1, 100)))
            lines.append(f"[{ts} {lvl}: {msg}")
        elif choice < 0.6:
            # Missing ':'
            ts = "".join(random.choices(chars.replace("]", ""), k=random.randint(1, 20)))
            lvl = "".join(random.choices(chars.replace(":", ""), k=random.randint(1, 10)))
            msg = "".join(random.choices(chars, k=random.randint(1, 100)))
            lines.append(f"[{ts}] {lvl} {msg}")
        elif choice < 0.8:
            # Very long line (up to 2048)
            lines.append("".join(random.choices(chars, k=random.randint(1025, 2048))))
        else:
            # Completely random garbage
            lines.append("".join(random.choices(chars, k=random.randint(0, 500))))

    return "\n".join(lines).encode('utf-8') + b"\n"

def test_log_parser_fuzz_equivalence():
    """Fuzz the agent's log parser against the oracle."""
    agent_path = "/home/user/log_parser"
    oracle_path = "/app/oracle_log_parser"

    assert os.path.isfile(oracle_path), "Oracle binary missing."

    fuzz_input = generate_fuzz_lines(10000)

    try:
        oracle_proc = subprocess.run([oracle_path], input=fuzz_input, capture_output=True, timeout=10)
        oracle_stdout = oracle_proc.stdout
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle program timed out. This is unexpected.")

    try:
        agent_proc = subprocess.run([agent_path], input=fuzz_input, capture_output=True, timeout=10)
        agent_stdout = agent_proc.stdout
    except subprocess.TimeoutExpired:
        pytest.fail("Agent program timed out on fuzz inputs. It might be stuck in an infinite loop.")

    if agent_proc.returncode != oracle_proc.returncode:
        pytest.fail(f"Agent return code ({agent_proc.returncode}) differs from oracle ({oracle_proc.returncode}). Did it crash?")

    if agent_stdout != oracle_stdout:
        # Find the first differing line to provide a helpful error message
        oracle_lines = oracle_stdout.split(b'\n')
        agent_lines = agent_stdout.split(b'\n')
        input_lines = fuzz_input.split(b'\n')

        for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
            if o_line != a_line:
                inp = input_lines[i].decode('utf-8', errors='replace')
                o_str = o_line.decode('utf-8', errors='replace')
                a_str = a_line.decode('utf-8', errors='replace')
                pytest.fail(f"Output mismatch on input line {i+1}.\nInput: {inp}\nExpected (Oracle): {o_str}\nGot (Agent): {a_str}")

        # If lengths differ
        pytest.fail(f"Output line count mismatch. Oracle lines: {len(oracle_lines)}, Agent lines: {len(agent_lines)}")