# test_final_state.py

import os
import subprocess
import random
import pytest

def test_integrator_fixed():
    integrator_path = "/app/adaptive_solve/adaptive_solve/integrator.py"
    assert os.path.isfile(integrator_path), f"File {integrator_path} is missing."
    with open(integrator_path, "r") as f:
        content = f.read()

    assert "h = h * (tol / err)**0.5" in content, "The integrator.py file does not contain the fixed logic."
    assert "h = h * (err / tol)**0.5" not in content, "The integrator.py file still contains the perturbed logic."

def test_fuzz_equivalence():
    agent_script = "/home/user/solve.py"
    oracle_script = "/oracle/solve.py"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} is missing."

    random.seed(42)
    bases = ['A', 'C', 'G', 'T']

    for i in range(30):
        num_args = random.randint(3, 6)
        args = []
        for _ in range(num_args):
            length = random.randint(5, 15)
            seq = "".join(random.choices(bases, k=length))
            args.append(seq)

        agent_cmd = ["python3", agent_script] + args
        oracle_cmd = ["python3", oracle_script] + args

        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)

        assert agent_proc.returncode == 0, f"Agent script failed on input {args}. Stderr: {agent_proc.stderr}"
        assert oracle_proc.returncode == 0, f"Oracle script failed on input {args}. Stderr: {oracle_proc.stderr}"

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        assert agent_out == oracle_out, f"Mismatch on input {args}.\nExpected:\n{oracle_out}\nGot:\n{agent_out}"