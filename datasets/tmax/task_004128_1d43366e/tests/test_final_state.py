# test_final_state.py

import subprocess
import random
import os
import pytest

def test_fuzz_equivalence():
    agent_bin = "/home/user/dataset_tool"
    oracle_bin = "/app/ref_tool"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"

    os.makedirs("/tmp/oracle_out", exist_ok=True)
    os.makedirs("/tmp/agent_out", exist_ok=True)

    random.seed(42)
    oracle_cmds = []
    agent_cmds = []

    # Generate fuzzing inputs
    inputs = []
    for i in range(1000):
        offset = random.randrange(0, 10000000 + 1, 2)
        length = random.randrange(100, 500000 + 1, 2)
        scale = random.uniform(0.1, 10.0)
        inputs.append((offset, length, scale))

        oracle_cmds.append(f"extract {offset} {length} {scale:.6f} /tmp/oracle_out/{i}.raw\n")
        agent_cmds.append(f"extract {offset} {length} {scale:.6f} /tmp/agent_out/{i}.raw\n")

    # Run oracle
    oracle_proc = subprocess.run([oracle_bin], input="".join(oracle_cmds), text=True, capture_output=True)
    assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr}"

    # Run agent
    agent_proc = subprocess.run([agent_bin], input="".join(agent_cmds), text=True, capture_output=True)
    assert agent_proc.returncode == 0, f"Agent program crashed or failed: {agent_proc.stderr}"

    # Compare outputs
    for i in range(1000):
        offset, length, scale = inputs[i]
        oracle_file = f"/tmp/oracle_out/{i}.raw"
        agent_file = f"/tmp/agent_out/{i}.raw"

        assert os.path.exists(oracle_file), f"Oracle failed to produce {oracle_file}"
        assert os.path.exists(agent_file), (
            f"Agent failed to produce output file for instruction: "
            f"extract {offset} {length} {scale:.6f} {agent_file}\n"
            f"Agent stderr: {agent_proc.stderr}"
        )

        with open(oracle_file, "rb") as f:
            oracle_data = f.read()
        with open(agent_file, "rb") as f:
            agent_data = f.read()

        if oracle_data != agent_data:
            pytest.fail(
                f"Output mismatch on instruction {i}:\n"
                f"Command: extract {offset} {length} {scale:.6f} <output_path>\n"
                f"Oracle output size: {len(oracle_data)} bytes\n"
                f"Agent output size: {len(agent_data)} bytes\n"
                f"Data differs!"
            )