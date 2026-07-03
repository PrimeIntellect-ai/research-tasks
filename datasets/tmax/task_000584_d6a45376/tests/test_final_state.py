# test_final_state.py
import os
import subprocess
import random
import pytest

def test_peewee_fixed():
    peewee_path = '/app/peewee/peewee.py'
    assert os.path.isfile(peewee_path), f"File {peewee_path} is missing."
    with open(peewee_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "INNNER" not in content, "The perturbation 'INNNER' was not fixed in peewee.py."

def test_fuzz_equivalence():
    agent_script = '/home/user/get_metrics.py'
    oracle_script = '/opt/oracle/get_metrics_oracle.py'

    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} is missing."

    datacenters = ['us-east-1', 'eu-west-1', 'ap-south-1', 'us-west-2', 'unknown-dc', 'drop table servers;']
    random.seed(42)

    for i in range(100):
        dc = random.choice(datacenters)
        min_size = random.randint(0, 5000000000)

        args = [str(dc), str(min_size)]

        # Run oracle
        oracle_cmd = ['python3', oracle_script] + args
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed unexpectedly on inputs {args}:\n{oracle_res.stderr}"

        # Run agent
        agent_cmd = ['python3', agent_script] + args
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert agent_res.returncode == 0, f"Agent script failed on inputs {args}:\n{agent_res.stderr}"

        assert agent_res.stdout == oracle_res.stdout, (
            f"Output mismatch on inputs {args} (iteration {i}).\n"
            f"Expected (Oracle):\n{oracle_res.stdout}\n"
            f"Got (Agent):\n{agent_res.stdout}"
        )