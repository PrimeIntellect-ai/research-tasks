# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_deployer_env_configured():
    env_path = "/home/user/deployer.env"
    assert os.path.exists(env_path), f"{env_path} does not exist"

    with open(env_path, "r") as f:
        content = f.read()

    assert 'FILTER_CMD="/home/user/mutator"' in content, f"Expected FILTER_CMD=\"/home/user/mutator\" in {env_path}"

def test_deployer_reload_triggered():
    reload_path = "/home/user/deployer.reload"
    assert os.path.exists(reload_path), f"{reload_path} was not created to trigger reload"

def test_mutator_executable_exists():
    mutator_path = "/home/user/mutator"
    assert os.path.exists(mutator_path), f"Executable {mutator_path} does not exist"
    assert os.access(mutator_path, os.X_OK), f"{mutator_path} is not executable"

def generate_fuzz_input():
    choice = random.random()
    if choice < 0.4:
        # Pod with spec.containers
        containers = []
        for _ in range(random.randint(0, 5)):
            image = f"image_{random.randint(1, 100)}"
            if random.random() < 0.5:
                image += ":latest"
            else:
                image += f":v{random.randint(1, 10)}"

            container = {
                "name": f"container_{random.randint(1, 100)}",
                "image": image
            }
            # Sometimes add extra fields
            if random.random() < 0.3:
                container["env"] = [{"name": "FOO", "value": "BAR"}]
            containers.append(container)

        obj = {
            "kind": "Pod",
            "apiVersion": "v1",
            "metadata": {"name": f"pod_{random.randint(1, 100)}"},
            "spec": {"containers": containers}
        }
        # Sometimes add other fields
        if random.random() < 0.3:
            obj["status"] = {"phase": "Pending"}
        return json.dumps(obj)
    elif choice < 0.7:
        # Deployment or other
        obj = {
            "kind": random.choice(["Deployment", "Service", "ConfigMap", "StatefulSet"]),
            "apiVersion": "apps/v1",
            "metadata": {"name": f"res_{random.randint(1, 100)}"},
            "spec": {
                "replicas": random.randint(1, 5),
                "template": {
                    "spec": {
                        "containers": [{"name": "c1", "image": "img:latest"}]
                    }
                }
            }
        }
        return json.dumps(obj)
    else:
        # Deeply nested or empty
        if random.random() < 0.2:
            return "{}"

        def make_nested(depth):
            if depth == 0:
                return random.choice(["val", 42, True, None, "latest", ":latest"])
            if random.random() < 0.5:
                return {f"key_{random.randint(1, 10)}": make_nested(depth - 1) for _ in range(random.randint(1, 4))}
            else:
                return [make_nested(depth - 1) for _ in range(random.randint(1, 4))]

        return json.dumps(make_nested(random.randint(2, 6)))

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_mutator"
    agent_path = "/home/user/mutator"

    assert os.path.exists(oracle_path), f"Oracle {oracle_path} not found"
    assert os.path.exists(agent_path), f"Agent binary {agent_path} not found"

    random.seed(42)

    for i in range(1000):
        input_json = generate_fuzz_input()
        input_bytes = input_json.encode('utf-8')

        oracle_proc = subprocess.run([oracle_path], input=input_bytes, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_bytes, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {input_json}"

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent crashed or failed (returncode {agent_proc.returncode}) on input:\n{input_json}\nStderr:\n{agent_proc.stderr.decode('utf-8', errors='replace')}")

        oracle_out = oracle_proc.stdout.decode('utf-8')
        agent_out = agent_proc.stdout.decode('utf-8')

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input:\n{input_json}\n"
                f"Oracle output:\n{oracle_out}\n"
                f"Agent output:\n{agent_out}\n"
            )