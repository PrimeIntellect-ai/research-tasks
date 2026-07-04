# test_final_state.py
import os
import random
import string
import subprocess

def test_files_exist():
    assert os.path.isfile("/home/user/auth_lib/libauth.so"), "libauth.so was not compiled or is missing."
    assert os.path.isfile("/home/user/solve.py"), "solve.py is missing."

def test_fuzz_equivalence():
    # Generate 100 random inputs
    random.seed(42)
    inputs = []
    for _ in range(100):
        length = random.randint(1, 50)
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        inputs.append(token)

    input_data = '\n'.join(inputs) + '\n'

    # Run oracle
    oracle_proc = subprocess.run(
        ["/app/oracle"],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr}"

    # Run agent's script
    agent_proc = subprocess.run(
        ["python3", "/home/user/solve.py"],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert agent_proc.returncode == 0, f"Agent script failed: {agent_proc.stderr}"

    oracle_lines = oracle_proc.stdout.strip().split('\n')
    agent_lines = agent_proc.stdout.strip().split('\n')

    assert len(oracle_lines) == len(inputs), "Oracle did not output the expected number of lines."
    assert len(agent_lines) == len(inputs), "Agent script did not output the expected number of lines."

    for i, (oracle_out, agent_out) in enumerate(zip(oracle_lines, agent_lines)):
        assert oracle_out == agent_out, (
            f"Mismatch on input '{inputs[i]}'. "
            f"Expected: {oracle_out}, Got: {agent_out}"
        )