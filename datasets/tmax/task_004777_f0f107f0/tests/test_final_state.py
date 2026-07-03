# test_final_state.py

import os
import subprocess
import random
import pytest

def test_sandbox_runner_compiled():
    runner_path = "/usr/local/bin/sandbox-runner"
    assert os.path.isfile(runner_path), f"sandbox-runner executable not found at {runner_path}"
    assert os.access(runner_path, os.X_OK), f"{runner_path} is not executable"

    # Test execution to ensure it correctly runs the sandboxed command
    result = subprocess.run([runner_path, "echo", "isolated"], capture_output=True, text=True)
    assert result.returncode == 0, f"sandbox-runner failed to execute, stderr: {result.stderr}"
    assert "isolated" in result.stdout, "sandbox-runner did not correctly execute the command"

def test_decoder_fuzz_equivalence():
    agent_script = "/home/user/decode_trace.py"
    oracle_bin = "/app/oracle/malware_decoder"

    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    random.seed(42)

    for i in range(200):
        length = random.randint(16, 4096)
        test_input = bytes(random.getrandbits(8) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=test_input,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"

        # Run agent
        agent_proc = subprocess.run(
            ["/usr/bin/python3", agent_script],
            input=test_input,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on iteration {i}. Stderr: {agent_proc.stderr.decode(errors='ignore')}"

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Mismatch on iteration {i} (input length {length}).\n"
            f"Oracle output length: {len(oracle_proc.stdout)}\n"
            f"Agent output length: {len(agent_proc.stdout)}"
        )