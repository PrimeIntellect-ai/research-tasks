# test_final_state.py

import os
import json
import random
import subprocess
import tempfile
import pytest

def test_config_files():
    # Check API .env
    env_path = "/app/api/.env"
    assert os.path.isfile(env_path), f"{env_path} is missing"
    with open(env_path, "r") as f:
        env_content = f.read()
    assert "REDIS_URL" in env_content, "REDIS_URL not found in /app/api/.env"
    assert "127.0.0.1:6379" in env_content or "localhost:6379" in env_content, "REDIS_URL does not point to local redis"

    # Check notebooks config.json
    config_path = "/app/notebooks/config.json"
    assert os.path.isfile(config_path), f"{config_path} is missing"
    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{config_path} is not valid JSON")

    assert "SIMULATION_API_URL" in config, "SIMULATION_API_URL missing in config.json"
    assert "8000" in config["SIMULATION_API_URL"], "SIMULATION_API_URL does not point to port 8000"

def test_validation_scripts_exist():
    assert os.path.isfile("/home/user/validate_distributions.py"), "/home/user/validate_distributions.py is missing"
    assert os.path.isfile("/home/user/divergence_report.txt"), "/home/user/divergence_report.txt is missing"

def test_fuzz_equivalence():
    agent_script = "/home/user/fixed_integrator.py"
    oracle_bin = "/app/oracle/integrator_reference"

    assert os.path.isfile(agent_script), f"{agent_script} is missing"
    assert os.path.isfile(oracle_bin), f"{oracle_bin} is missing"

    random.seed(42)
    N = 1000

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.json")
        agent_out = os.path.join(tmpdir, "agent_out.json")
        oracle_out = os.path.join(tmpdir, "oracle_out.json")

        for i in range(N):
            params = {
                "N_initial": random.randint(10, 1000),
                "growth_rate": random.uniform(0.1, 2.5),
                "max_steps": random.randint(10, 100),
                "tolerance": random.uniform(0.01, 0.1)
            }

            with open(input_path, "w") as f:
                json.dump(params, f)

            # Run oracle
            oracle_proc = subprocess.run(
                [oracle_bin, input_path, oracle_out],
                capture_output=True, text=True
            )
            assert oracle_proc.returncode == 0, f"Oracle failed on input {params}:\n{oracle_proc.stderr}"

            # Run agent
            agent_proc = subprocess.run(
                ["/usr/bin/python3", agent_script, input_path, agent_out],
                capture_output=True, text=True
            )
            assert agent_proc.returncode == 0, f"Agent script failed on input {params}:\n{agent_proc.stderr}"

            # Compare outputs
            assert os.path.isfile(oracle_out), "Oracle did not produce output file"
            assert os.path.isfile(agent_out), "Agent did not produce output file"

            with open(oracle_out, "r") as f:
                oracle_data = f.read()
            with open(agent_out, "r") as f:
                agent_data = f.read()

            assert oracle_data == agent_data, (
                f"Mismatch on iteration {i} with input {params}.\n"
                f"Oracle output:\n{oracle_data}\n"
                f"Agent output:\n{agent_data}"
            )