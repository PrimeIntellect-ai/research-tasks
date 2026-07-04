# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def generate_fuzz_inputs(n=100, seed=42):
    random.seed(seed)
    inputs = []
    bases = ['A', 'C', 'G', 'T']
    for _ in range(n):
        primer_len = random.randint(3, 6)
        primer = "".join(random.choices(bases, k=primer_len))
        seq_len = random.randint(20, 50)

        if random.random() < 0.5:
            # Insert primer into sequence to ensure a match
            seq_list = random.choices(bases, k=seq_len)
            insert_idx = random.randint(0, seq_len - primer_len)
            seq_list[insert_idx:insert_idx+primer_len] = list(primer)
            sequence = "".join(seq_list)
        else:
            # Generate random sequence (might still contain primer by chance, which is fine)
            sequence = "".join(random.choices(bases, k=seq_len))

        signal = [random.uniform(-10.0, 10.0) for _ in range(len(sequence))]

        inputs.append({
            "primer": primer,
            "sequence": sequence,
            "signal": signal
        })
    return inputs

def test_fuzz_equivalence():
    agent_script = "/home/user/prepare_data.py"
    oracle_script = "/opt/oracle/prepare_data.py"

    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script not found at {oracle_script}"

    inputs = generate_fuzz_inputs(n=100, seed=1337)
    input_str = "\n".join(json.dumps(x) for x in inputs) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        ["python3", oracle_script],
        input=input_str,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed to run, perhaps the package bug is not fully fixed? Error:\n{oracle_proc.stderr}"

    # Run agent
    agent_proc = subprocess.run(
        ["python3", agent_script],
        input=input_str,
        text=True,
        capture_output=True
    )
    assert agent_proc.returncode == 0, f"Agent script failed to run. Error:\n{agent_proc.stderr}"

    oracle_lines = oracle_proc.stdout.strip().split('\n')
    agent_lines = agent_proc.stdout.strip().split('\n')

    assert len(oracle_lines) == len(agent_lines), f"Mismatched number of output lines. Oracle produced {len(oracle_lines)}, Agent produced {len(agent_lines)}."

    for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
        assert o_line == a_line, (
            f"Output mismatch on input {i+1}.\n"
            f"Input JSON: {json.dumps(inputs[i])}\n"
            f"Oracle output: {o_line}\n"
            f"Agent output:  {a_line}"
        )