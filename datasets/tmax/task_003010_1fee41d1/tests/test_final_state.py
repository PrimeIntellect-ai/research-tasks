# test_final_state.py
import json
import random
import subprocess
import os

def test_fuzz_equivalence():
    agent_script = "/home/user/update_model.py"
    oracle_script = "/app/oracle_update_model.py"

    assert os.path.exists(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.exists(oracle_script), f"Oracle script missing: {oracle_script}"

    random.seed(42)
    N = 1000

    for i in range(N):
        temp = random.uniform(10.0, 30.0)
        obs_length = random.randint(0, 100)
        obs = [random.choice([0, 1]) for _ in range(obs_length)]

        input_data = json.dumps({"temp": temp, "obs": obs})

        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=input_data,
            text=True,
            capture_output=True
        )

        oracle_proc = subprocess.run(
            ["python3", oracle_script],
            input=input_data,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed on input: {input_data}\nStderr: {agent_proc.stderr}"
        assert oracle_proc.returncode == 0, f"Oracle script failed on input: {input_data}\nStderr: {oracle_proc.stderr}"

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        try:
            agent_json = json.loads(agent_out)
        except json.JSONDecodeError:
            assert False, f"Agent output is not valid JSON.\nInput: {input_data}\nOutput: {agent_out}"

        try:
            oracle_json = json.loads(oracle_out)
        except json.JSONDecodeError:
            assert False, f"Oracle output is not valid JSON.\nInput: {input_data}\nOutput: {oracle_out}"

        assert agent_json == oracle_json, (
            f"Mismatch on input: {input_data}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )