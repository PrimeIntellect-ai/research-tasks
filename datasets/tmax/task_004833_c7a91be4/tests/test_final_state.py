# test_final_state.py
import os
import subprocess
import random
import pytest

def test_anomaly_report():
    report_path = "/home/user/ticket_4092/anomaly_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."
    with open(report_path, "r") as f:
        content = f.read().strip()

    expected = "145\n146\n147"
    assert content == expected, f"Anomaly report content is incorrect. Expected:\n{expected}\nGot:\n{content}"

def test_detector_fuzz_equivalence():
    agent_bin = "/home/user/ticket_4092/detector"
    oracle_bin = "/app/oracle_detector"

    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} does not exist."
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."

    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} does not exist."
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable."

    random.seed(42)
    N = 1000

    for i in range(N):
        num_ints = random.randint(0, 100)
        input_data = bytearray()
        for _ in range(num_ints):
            # Generate a random 64-bit integer, emphasizing values around the threshold 200
            if random.random() < 0.2:
                val = random.randint(190, 210)
            else:
                val = random.randint(0, (1 << 64) - 1)
            input_data.extend(val.to_bytes(8, byteorder='little'))

        input_bytes = bytes(input_data)

        # Run agent
        agent_proc = subprocess.run([agent_bin], input=input_bytes, capture_output=True)
        # Run oracle
        oracle_proc = subprocess.run([oracle_bin], input=input_bytes, capture_output=True)

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on input {i}: agent={agent_proc.returncode}, oracle={oracle_proc.returncode}"
        assert agent_proc.stdout == oracle_proc.stdout, f"Stdout mismatch on input {i}:\nInput length: {len(input_bytes)} bytes\nAgent stdout: {agent_proc.stdout}\nOracle stdout: {oracle_proc.stdout}"
        assert agent_proc.stderr == oracle_proc.stderr, f"Stderr mismatch on input {i}:\nAgent stderr: {agent_proc.stderr}\nOracle stderr: {oracle_proc.stderr}"