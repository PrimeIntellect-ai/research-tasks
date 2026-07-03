# test_final_state.py

import os
import json
import random
import subprocess
import yaml

def test_docker_compose_fixed():
    compose_path = '/home/user/services/docker-compose.yml'
    assert os.path.isfile(compose_path), f"Expected docker-compose file at {compose_path}"

    with open(compose_path, 'r') as f:
        compose_data = yaml.safe_load(f)

    services = compose_data.get('services', {})
    metadata_store = services.get('metadata_store', {})
    model_repo = services.get('model_repo', {})

    # Check port mappings
    redis_ports = metadata_store.get('ports', [])
    nginx_ports = model_repo.get('ports', [])

    assert any(str(p).startswith('6379:') or str(p) == '6379' for p in redis_ports), "metadata_store must expose port 6379"
    assert any(str(p).startswith('8080:') or str(p) == '8080' for p in nginx_ports), "model_repo must expose port 8080"


def test_fuzz_equivalence():
    agent_script = '/home/user/cli.py'
    oracle_script = '/app/oracle_cli.py'

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist"
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} does not exist"

    random.seed(42)
    num_tests = 500

    for i in range(num_tests):
        num_objects = random.randint(1, 50)
        input_data = []
        for _ in range(num_objects):
            if random.random() < 0.3:
                item_id = None
            else:
                item_id = random.randint(1, 100)
            feature_val = random.uniform(-10.0, 10.0)
            input_data.append({"item_id": item_id, "feature_val": feature_val})

        input_json = json.dumps(input_data)

        # Run oracle
        oracle_proc = subprocess.run(
            ['python3', oracle_script],
            input=input_json,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {input_json}. Stderr: {oracle_proc.stderr}"
        oracle_output = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ['python3', agent_script],
            input=input_json,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input {input_json}. Stderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout.strip()

        assert agent_output == oracle_output, (
            f"Output mismatch on test {i+1}/{num_tests}.\n"
            f"Input: {input_json}\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output: {agent_output}"
        )