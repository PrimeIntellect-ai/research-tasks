# test_final_state.py

import os
import subprocess
import random
import pytest
import re

def test_files_exist():
    assert os.path.isfile("/app/payload_transform.c"), "Missing /app/payload_transform.c"
    assert os.path.isfile("/app/Makefile"), "Missing /app/Makefile"

def test_makefile_targets():
    # Clean up any existing binaries to ensure make actually builds them
    for binary in ["/app/payload_transform", "/app/payload_benchmark"]:
        if os.path.exists(binary):
            os.remove(binary)

    # Test default target 'all'
    result_all = subprocess.run(["make", "all"], cwd="/app", capture_output=True, text=True)
    assert result_all.returncode == 0, f"make all failed:\n{result_all.stderr}"
    assert os.path.isfile("/app/payload_transform"), "make all did not produce /app/payload_transform"
    assert os.access("/app/payload_transform", os.X_OK), "/app/payload_transform is not executable"

    # Test 'benchmark' target
    result_bench = subprocess.run(["make", "benchmark"], cwd="/app", capture_output=True, text=True)
    assert result_bench.returncode == 0, f"make benchmark failed:\n{result_bench.stderr}"
    assert os.path.isfile("/app/payload_benchmark"), "make benchmark did not produce /app/payload_benchmark"
    assert os.access("/app/payload_benchmark", os.X_OK), "/app/payload_benchmark is not executable"

def test_benchmark_output():
    # Ensure benchmark runs and outputs an integer
    result = subprocess.run(["/app/payload_benchmark"], capture_output=True, text=True)
    assert result.returncode == 0, f"payload_benchmark failed to run:\n{result.stderr}"
    output = result.stdout.strip()
    assert re.fullmatch(r"\d+", output), f"payload_benchmark output is not a single integer (milliseconds): {output}"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_payload_transform"
    agent_path = "/app/payload_transform"

    assert os.path.isfile(oracle_path), f"Oracle missing: {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle not executable: {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing: {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary not executable: {agent_path}"

    random.seed(42)
    N = 500

    for i in range(N):
        length = random.randint(1, 4096)
        input_data = bytes(random.choices(range(256), k=length))

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"
        assert agent_proc.returncode == 0, f"Agent program failed on iteration {i} with error: {agent_proc.stderr.decode(errors='replace')}"

        oracle_out = oracle_proc.stdout
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on iteration {i} (input length {length}).\n"
                f"Input (hex): {input_data.hex()[:100]}...\n"
                f"Oracle output: {oracle_out.decode(errors='replace')[:100]}...\n"
                f"Agent output: {agent_out.decode(errors='replace')[:100]}..."
            )