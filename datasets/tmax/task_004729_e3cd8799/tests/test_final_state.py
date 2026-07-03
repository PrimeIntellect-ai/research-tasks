# test_final_state.py

import os
import random
import subprocess
import pytest
import re

def generate_payload():
    num_instructions = random.randint(4, 100)
    payload = ""
    for _ in range(num_instructions):
        if random.random() < 0.05:
            payload += "FF"
            break

        op = random.choice(["01", "02", "03", "04", "05"])
        payload += op
        if op in ["01", "02", "05"]:
            payload += f"{random.randint(0, 255):02X}"
    return payload

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_chksum_bin"
    agent_path = "/home/user/bash_parser.sh"

    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} is missing."
    assert os.path.isfile(agent_path), f"Agent script {agent_path} is missing."

    random.seed(42)

    for i in range(1000):
        payload = generate_payload()

        oracle_res = subprocess.run([oracle_path, payload], capture_output=True, text=True)
        agent_res = subprocess.run(["/bin/bash", agent_path, payload], capture_output=True, text=True)

        assert oracle_res.returncode == agent_res.returncode, (
            f"Exit code mismatch on payload: {payload}\n"
            f"Oracle exit code: {oracle_res.returncode}\n"
            f"Agent exit code: {agent_res.returncode}"
        )
        assert oracle_res.stdout == agent_res.stdout, (
            f"Stdout mismatch on payload: {payload}\n"
            f"Oracle stdout:\n{oracle_res.stdout}\n"
            f"Agent stdout:\n{agent_res.stdout}"
        )

def test_benchmark_artifacts():
    benchmark_script = "/home/user/benchmark.sh"
    benchmark_log = "/home/user/benchmark_results.log"

    assert os.path.isfile(benchmark_script), f"Benchmark script {benchmark_script} is missing."
    assert os.path.isfile(benchmark_log), f"Benchmark log {benchmark_log} is missing."

    with open(benchmark_log, "r") as f:
        content = f.read().strip()

    lines = content.split('\n')
    assert len(lines) >= 1, "Benchmark log is empty."

    last_line = lines[-1]
    pattern = r"^Legacy: [0-9.]+s \| Bash: [0-9.]+s$"
    assert re.match(pattern, last_line), f"Benchmark log format is incorrect. Found: {last_line}"