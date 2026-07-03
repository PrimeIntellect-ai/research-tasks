# test_final_state.py
import os
import subprocess
import random

def test_fast_extractor_fuzz_equivalence():
    oracle_path = "/app/oracle_extractor"
    agent_path = "/home/user/fast_extractor"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent executable missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent file at {agent_path} is not executable"

    random.seed(42)
    N = 50
    min_length = 1000
    max_length = 15000
    min_val = -32768
    max_val = 32767

    for i in range(N):
        length = random.randint(min_length, max_length)
        input_array = [str(random.randint(min_val, max_val)) for _ in range(length)]
        input_str = " ".join(input_array) + "\n"

        oracle_proc = subprocess.run([oracle_path], input=input_str, text=True, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_str, text=True, capture_output=True)

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on fuzz test {i+1}/{N}.\n"
            f"Input length: {length}\n"
            f"Oracle output: {oracle_out[:100]}...\n"
            f"Agent output: {agent_out[:100]}...\n"
        )

def test_other_files_exist():
    assert os.path.exists("/home/user/transcript.txt"), "Transcript file /home/user/transcript.txt is missing"
    assert os.path.exists("/home/user/plot_features.py"), "Plotting script /home/user/plot_features.py is missing"
    assert os.path.exists("/home/user/sec_plot.png"), "Plot image /home/user/sec_plot.png is missing"