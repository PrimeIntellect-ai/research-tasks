# test_final_state.py
import os
import random
import subprocess
import pytest

def test_go_calc_exists_and_executable():
    agent_bin = "/app/bin/go_calc"
    assert os.path.isfile(agent_bin), f"Expected Go binary at {agent_bin} does not exist."
    assert os.access(agent_bin, os.X_OK), f"Go binary at {agent_bin} is not executable."

def test_fuzz_equivalence():
    oracle_bin = "/app/bin/legacy_calc"
    agent_bin = "/app/bin/go_calc"

    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} is missing."

    random.seed(42)

    def generate_expr(depth=0):
        if depth > 2 or random.random() < 0.4:
            return str(random.randint(1, 1000))
        op = random.choice([' + ', ' - ', ' * ', ' / '])
        left = generate_expr(depth + 1)
        right = generate_expr(depth + 1)
        expr = f"{left}{op}{right}"
        if random.random() < 0.3:
            expr = f"({expr})"
        return expr

    valid_exprs = []
    # Generate 2000 valid expressions that the oracle can successfully evaluate
    # (this naturally filters out division by zero and other potential C-level crashes)
    while len(valid_exprs) < 2000:
        expr = generate_expr()
        if len(expr) > 50:
            continue

        try:
            res = subprocess.run([oracle_bin, expr], capture_output=True, text=True, timeout=0.5)
            if res.returncode == 0 and "Result:" in res.stdout and "Checksum:" in res.stdout:
                valid_exprs.append(expr)
        except subprocess.TimeoutExpired:
            pass
        except Exception:
            pass

    # Now verify the agent matches the oracle on all 2000 inputs
    for expr in valid_exprs:
        oracle_res = subprocess.run([oracle_bin, expr], capture_output=True, text=True)
        agent_res = subprocess.run([agent_bin, expr], capture_output=True, text=True)

        assert agent_res.returncode == 0, f"Agent crashed or failed on input '{expr}'.\nStderr: {agent_res.stderr}"
        assert oracle_res.stdout == agent_res.stdout, (
            f"Mismatch on input '{expr}'\n"
            f"Oracle output: {oracle_res.stdout.strip()}\n"
            f"Agent output:  {agent_res.stdout.strip()}"
        )