# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def generate_random_string(min_length=5, max_length=100):
    charset = string.ascii_letters + string.digits + " "
    length = random.randint(min_length, max_length)
    return "".join(random.choice(charset) for _ in range(length))

def test_fuzz_equivalence():
    oracle_cmd = ["/app/legacy_scorer"]
    agent_cmd = ["python3", "/home/user/scorer.py"]

    assert os.path.exists("/home/user/scorer.py"), "Agent script /home/user/scorer.py is missing."

    random.seed(42)
    for _ in range(100):
        input_str = generate_random_string()
        input_bytes = input_str.encode('utf-8')

        oracle_res = subprocess.run(oracle_cmd, input=input_bytes, capture_output=True)
        agent_res = subprocess.run(agent_cmd, input=input_bytes, capture_output=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input '{input_str}'."
        assert agent_res.returncode == 0, f"Agent script failed on input '{input_str}'.\nStderr: {agent_res.stderr.decode('utf-8', errors='replace')}"

        oracle_out = oracle_res.stdout.decode('utf-8').strip()
        agent_out = agent_res.stdout.decode('utf-8').strip()

        assert oracle_out == agent_out, f"Mismatch on input '{input_str}'.\nExpected: {oracle_out}\nGot: {agent_out}"

def test_plot_anomalies_fixed():
    plot_script = "/home/user/plot_anomalies.py"
    plot_output = "/home/user/plot.png"

    assert os.path.exists(plot_script), f"Missing file: {plot_script}"

    if os.path.exists(plot_output):
        os.remove(plot_output)

    res = subprocess.run(["python3", plot_script], capture_output=True)
    assert res.returncode == 0, f"plot_anomalies.py failed.\nStderr: {res.stderr.decode('utf-8', errors='replace')}"

    assert os.path.exists(plot_output), f"{plot_output} was not created."
    assert os.path.getsize(plot_output) > 100, f"{plot_output} is suspiciously small (likely blank or corrupted)."

    with open(plot_output, "rb") as f:
        header = f.read(8)
        assert header == b"\x89PNG\r\n\x1a\n", f"{plot_output} is not a valid PNG file."