# test_final_state.py

import os
import json
import random
import base64
import subprocess
import tempfile
import pytest

def test_extractor_built():
    assert os.path.exists("/home/user/artifact-builder/extractor"), "The extractor binary was not built."
    assert os.access("/home/user/artifact-builder/extractor", os.X_OK), "The extractor is not executable."

def test_raw_events_generated():
    raw_events_path = "/home/user/raw_events.json"
    assert os.path.exists(raw_events_path), f"{raw_events_path} was not generated."

    with open(raw_events_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{raw_events_path} does not contain valid JSON.")

    assert isinstance(data, list), f"{raw_events_path} should contain a JSON array."

def generate_random_base64(length):
    raw_bytes = bytes(random.choices(range(256), k=length))
    return base64.b64encode(raw_bytes).decode('utf-8')

def generate_v1_array(num_elements):
    arr = []
    for _ in range(num_elements):
        arr.append({
            "frame_id": random.randint(0, 10000),
            "raw_data": generate_random_base64(random.randint(10, 50)),
            "timestamp": random.uniform(0.0, 3600.0)
        })
    return arr

def test_fuzz_equivalence_migration():
    oracle = "/app/oracle_migrate"
    agent = "/home/user/migrate/run_migration"

    assert os.path.exists(oracle), f"Oracle binary {oracle} not found."
    assert os.path.exists(agent), f"Agent binary {agent} not found."
    assert os.access(agent, os.X_OK), f"Agent binary {agent} is not executable."

    random.seed(42)
    # Run 50 iterations with varying array sizes to simulate 500 total elements
    for i in range(50):
        num_elements = random.randint(0, 20)
        data = generate_v1_array(num_elements)

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            json.dump(data, tmp)
            tmp_path = tmp.name

        try:
            oracle_proc = subprocess.run([oracle, tmp_path], capture_output=True, text=True)
            agent_proc = subprocess.run([agent, tmp_path], capture_output=True, text=True)

            assert agent_proc.returncode == oracle_proc.returncode, (
                f"Return code mismatch on iteration {i}.\n"
                f"Input data: {data}\n"
                f"Oracle return code: {oracle_proc.returncode}\n"
                f"Agent return code: {agent_proc.returncode}\n"
                f"Agent stderr: {agent_proc.stderr}"
            )

            if oracle_proc.returncode == 0:
                try:
                    oracle_json = json.loads(oracle_proc.stdout)
                except json.JSONDecodeError:
                    oracle_json = oracle_proc.stdout.strip()

                try:
                    agent_json = json.loads(agent_proc.stdout)
                except json.JSONDecodeError:
                    agent_json = agent_proc.stdout.strip()

                assert agent_json == oracle_json, (
                    f"Output mismatch on iteration {i}.\n"
                    f"Input data: {data}\n"
                    f"Expected (Oracle): {oracle_json}\n"
                    f"Got (Agent): {agent_json}"
                )
        finally:
            os.remove(tmp_path)