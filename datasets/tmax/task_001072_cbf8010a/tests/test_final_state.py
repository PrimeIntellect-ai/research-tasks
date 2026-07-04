# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

def test_fastakit_fixed_and_installed():
    """Verify that the fastakit package is fixed and installed correctly."""
    # Create a temporary FASTA file to test the fix
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".fasta") as tmp:
        tmp.write(">test_seq\n")
        tmp.write("CGTA\n")
        tmp.write("CGTA\n")
        tmp_path = tmp.name

    try:
        # We run a small python snippet to test fastakit
        script = f"""
import sys
try:
    import fastakit
except ImportError:
    sys.exit(1)

try:
    seq_id, seq = fastakit.read_fasta("{tmp_path}")
    if "\\n" in seq:
        sys.exit(2)
    if not seq.endswith("A"):
        sys.exit(3)
    if seq != "CGTACGTA":
        sys.exit(4)
except Exception as e:
    sys.exit(5)
sys.exit(0)
"""
        result = subprocess.run(["python3", "-c", script], capture_output=True)
        assert result.returncode == 0, f"fastakit check failed with returncode {result.returncode}. Is it installed and fixed?"
    finally:
        os.remove(tmp_path)

def test_analyze_script_exists():
    """Verify that the analyze.py script exists."""
    script_path = "/home/user/analyze.py"
    assert os.path.isfile(script_path), f"Agent script {script_path} is missing."

def test_fuzz_equivalence():
    """Fuzz the agent's script against the oracle to ensure exact output match."""
    oracle_path = "/opt/oracle/dinuc_oracle"
    agent_script = "/home/user/analyze.py"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} is missing."
    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."

    random.seed(42)
    N = 100

    for i in range(N):
        seq_id = f"seq_{random.randint(0, 9999)}"
        seq_len = random.randint(100, 1000)
        seq_chars = [random.choice(['A', 'C', 'G', 'T']) for _ in range(seq_len)]

        # Wrap at 80 chars
        lines = []
        for j in range(0, seq_len, 80):
            lines.append("".join(seq_chars[j:j+80]))

        fasta_content = f">{seq_id}\n" + "\n".join(lines) + "\n"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".fasta") as tmp:
            tmp.write(fasta_content)
            tmp_path = tmp.name

        try:
            # Run oracle
            oracle_res = subprocess.run([oracle_path, tmp_path], capture_output=True, text=True)
            assert oracle_res.returncode == 0, f"Oracle failed on input {i}"
            oracle_out = oracle_res.stdout.strip()

            # Run agent
            agent_res = subprocess.run(["python3", agent_script, tmp_path], capture_output=True, text=True)
            assert agent_res.returncode == 0, f"Agent script failed on input {i}. Error: {agent_res.stderr}"
            agent_out = agent_res.stdout.strip()

            assert oracle_out == agent_out, (
                f"Mismatch on iteration {i}.\n"
                f"Input FASTA:\n{fasta_content}\n"
                f"Oracle Output:\n{oracle_out}\n"
                f"Agent Output:\n{agent_out}\n"
            )
        finally:
            os.remove(tmp_path)