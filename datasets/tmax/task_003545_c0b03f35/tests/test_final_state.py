# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

def test_seq_affinity_installed():
    try:
        import seq_affinity
    except ImportError as e:
        pytest.fail(f"seq_affinity package is not installed or importable. Error: {e}")

def test_fuzz_equivalence():
    agent_script = "/home/user/analyze.py"
    oracle_script = "/app/oracle_analyze.py"

    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script missing at {oracle_script}"

    random.seed(42)
    num_iterations = 20

    for i in range(num_iterations):
        num_seqs = random.randint(50, 200)
        seqs = []
        for _ in range(num_seqs):
            length = random.randint(20, 50)
            seq = "".join(random.choices(["A", "C", "G", "T"], k=length))
            seqs.append(seq)

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("\n".join(seqs) + "\n")
            input_path = f.name

        try:
            oracle_res = subprocess.run(
                ["python3", oracle_script, input_path],
                capture_output=True, text=True
            )
            assert oracle_res.returncode == 0, f"Oracle script failed on fuzz input {i}:\n{oracle_res.stderr}"

            agent_res = subprocess.run(
                ["python3", agent_script, input_path],
                capture_output=True, text=True
            )
            assert agent_res.returncode == 0, f"Agent script failed on fuzz input {i}:\n{agent_res.stderr}"

            oracle_out = oracle_res.stdout.strip()
            agent_out = agent_res.stdout.strip()

            assert agent_out == oracle_out, (
                f"Output mismatch on fuzz input {i}.\n"
                f"Input details: {num_seqs} sequences.\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output:  {agent_out}"
            )
        finally:
            os.remove(input_path)