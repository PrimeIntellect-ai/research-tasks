# test_final_state.py
import os
import random
import subprocess
import pytest

AGENT_EXTRACTOR = "/home/user/extractor"
ORACLE_EXTRACTOR = "/app/oracle_extractor"
NUM_TESTS = 1000

def generate_fasta_input(seed):
    random.seed(seed)
    length = random.randint(10, 1000)
    bases = ['A', 'C', 'G', 'T']

    seq = []
    for _ in range(length):
        seq.append(random.choice(bases))
        # Randomly insert newlines to test robustness
        if random.random() < 0.05:
            seq.append('\n')

    return ">seq\n" + "".join(seq)

def test_extractor_exists_and_executable():
    """Check that the agent's extractor executable exists and is executable."""
    assert os.path.isfile(AGENT_EXTRACTOR), f"Agent's executable not found at {AGENT_EXTRACTOR}"
    assert os.access(AGENT_EXTRACTOR, os.X_OK), f"Agent's file {AGENT_EXTRACTOR} is not executable"

def test_fuzz_equivalence():
    """Fuzz test the agent's extractor against the reference oracle."""
    assert os.path.isfile(ORACLE_EXTRACTOR), f"Oracle executable missing at {ORACLE_EXTRACTOR}"
    assert os.access(ORACLE_EXTRACTOR, os.X_OK), f"Oracle executable {ORACLE_EXTRACTOR} is not executable"

    for i in range(NUM_TESTS):
        fasta_input = generate_fasta_input(i)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_EXTRACTOR],
                input=fasta_input,
                text=True,
                capture_output=True,
                check=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle program timed out on input seed {i}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input seed {i}: {e.stderr}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_EXTRACTOR],
                input=fasta_input,
                text=True,
                capture_output=True,
                check=True,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input seed {i}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program crashed on input seed {i}: {e.stderr}")

        assert agent_out == oracle_out, (
            f"Mismatch on seed {i}.\n\n"
            f"Input:\n{fasta_input}\n\n"
            f"Expected Output (Oracle):\n{oracle_out}\n"
            f"Actual Output (Agent):\n{agent_out}"
        )