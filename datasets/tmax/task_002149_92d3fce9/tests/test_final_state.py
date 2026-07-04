# test_final_state.py

import os
import stat
import subprocess
import random
import string
import pytest

def generate_test_case():
    length = random.randint(10, 100)
    # Ensure spaces are included to test the regression
    chars = string.ascii_letters + string.digits + " \t\n!@#$%"
    return "ENCv1|" + "".join(random.choice(chars) for _ in range(length))

def run_proc(cmd, stdin_data):
    try:
        res = subprocess.run(
            cmd, 
            input=stdin_data.encode(), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            timeout=2
        )
        return res.stdout.decode().strip()
    except Exception:
        return None

def test_fixed_encode_exists_and_executable():
    fixed_script = "/home/user/fixed_encode.sh"
    assert os.path.exists(fixed_script), f"Fixed script {fixed_script} does not exist."
    assert os.path.isfile(fixed_script), f"{fixed_script} is not a file."

    st = os.stat(fixed_script)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), \
        f"Fixed script {fixed_script} is not executable."

def test_fixed_encode_accuracy():
    oracle_cmd = ["/app/oracle_processor"]
    agent_cmd = ["/home/user/fixed_encode.sh"]

    assert os.path.exists(oracle_cmd[0]), f"Oracle binary {oracle_cmd[0]} does not exist."

    correct = 0
    total = 50

    random.seed(42) # For reproducible test cases

    for _ in range(total):
        test_input = generate_test_case()

        oracle_out = run_proc(oracle_cmd, test_input)
        agent_out = run_proc(agent_cmd, test_input)

        assert oracle_out is not None, "Oracle processor failed to execute or timed out."

        if agent_out == oracle_out:
            correct += 1

    accuracy = correct / total
    assert accuracy >= 1.0, f"Accuracy metric failed: {accuracy} < 1.0. The fixed script output does not perfectly match the oracle for all valid inputs."

def test_missing_magic_string():
    oracle_cmd = ["/app/oracle_processor"]
    agent_cmd = ["/home/user/fixed_encode.sh"]

    test_input = "INVALID_MAGIC|some random data"
    oracle_out = run_proc(oracle_cmd, test_input)
    agent_out = run_proc(agent_cmd, test_input)

    assert oracle_out is not None, "Oracle processor failed to execute."
    assert agent_out == oracle_out, f"Expected output '{oracle_out}' for missing magic string, but got '{agent_out}'"