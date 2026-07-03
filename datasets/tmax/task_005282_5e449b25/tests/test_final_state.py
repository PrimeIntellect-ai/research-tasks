# test_final_state.py
import os
import random
import subprocess
import pytest

def test_signal_csv_exists():
    assert os.path.isfile("/home/user/signal.csv"), "The file /home/user/signal.csv is missing. Did you extract the video signal?"

def test_evaluate_ll_script_exists():
    assert os.path.isfile("/home/user/evaluate_ll.py"), "The script /home/user/evaluate_ll.py is missing."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_evaluate_ll"
    agent_script = "/home/user/evaluate_ll.py"

    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} missing."
    assert os.path.isfile(agent_script), f"Agent script {agent_script} missing."

    random.seed(42)

    for i in range(100):
        k1 = random.uniform(0.01, 2.0)
        k2 = random.uniform(0.01, 2.0)

        k1_str = f"{k1:.6f}"
        k2_str = f"{k2:.6f}"

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_path, k1_str, k2_str],
                capture_output=True, text=True, check=True, timeout=5
            )
            oracle_val = float(oracle_res.stdout.strip())
        except Exception as e:
            pytest.fail(f"Oracle failed on inputs k1={k1_str}, k2={k2_str}: {e}")

        # Run agent
        try:
            agent_res = subprocess.run(
                ["python3", agent_script, k1_str, k2_str],
                capture_output=True, text=True, check=True, timeout=5
            )
            agent_val = float(agent_res.stdout.strip())
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on inputs k1={k1_str}, k2={k2_str}. Stderr: {e.stderr}")
        except ValueError:
            pytest.fail(f"Agent script output could not be parsed as float on inputs k1={k1_str}, k2={k2_str}. Output: {agent_res.stdout}")
        except Exception as e:
            pytest.fail(f"Agent script error on inputs k1={k1_str}, k2={k2_str}: {e}")

        # Compare
        if abs(oracle_val - agent_val) > 1e-5:
            pytest.fail(
                f"Mismatch on inputs k1={k1_str}, k2={k2_str}.\n"
                f"Oracle output: {oracle_val}\n"
                f"Agent output:  {agent_val}\n"
                f"Difference:    {abs(oracle_val - agent_val)}"
            )