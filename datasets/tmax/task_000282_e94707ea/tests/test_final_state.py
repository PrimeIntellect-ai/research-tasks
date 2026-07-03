# test_final_state.py
import os
import subprocess
import random
import pytest

AGENT_EXECUTABLE = "/home/user/extractor"
ORACLE_EXECUTABLE = "/app/oracle_extractor"

def test_agent_executable_exists():
    assert os.path.exists(AGENT_EXECUTABLE), f"Agent executable missing at {AGENT_EXECUTABLE}. Did you compile your C++ code?"
    assert os.path.isfile(AGENT_EXECUTABLE), f"Path {AGENT_EXECUTABLE} is not a file."
    assert os.access(AGENT_EXECUTABLE, os.X_OK), f"Agent executable {AGENT_EXECUTABLE} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_EXECUTABLE), f"Oracle executable missing at {ORACLE_EXECUTABLE}. Setup issue."

    random.seed(42)
    # N = 20 random integers chosen uniformly between 1 and 30
    test_inputs = [random.randint(1, 30) for _ in range(20)]

    for t in test_inputs:
        cmd_oracle = [ORACLE_EXECUTABLE, str(t)]
        cmd_agent = [AGENT_EXECUTABLE, str(t)]

        try:
            res_oracle = subprocess.run(cmd_oracle, capture_output=True, text=True, check=True, timeout=15)
            out_oracle = res_oracle.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {t}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {t}")

        try:
            res_agent = subprocess.run(cmd_agent, capture_output=True, text=True, check=True, timeout=15)
            out_agent = res_agent.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input {t} (exit code {e.returncode}). Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input {t}")

        assert out_agent == out_oracle, (
            f"Output mismatch on input {t}.\n"
            f"Expected (Oracle): {out_oracle!r}\n"
            f"Got (Agent):       {out_agent!r}"
        )