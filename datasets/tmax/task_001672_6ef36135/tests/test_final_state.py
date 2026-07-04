# test_final_state.py

import os
import sys
import json
import random
import string
import subprocess
import pytest

def test_ujson_installed():
    """Verify that ujson was successfully installed and can be imported."""
    try:
        import ujson
        # Check basic functionality
        assert ujson.dumps({"test": 1}) == '{"test":1}', "ujson is installed but dumps() failed."
    except ImportError:
        pytest.fail("ujson is not installed. The agent failed to fix and install the package.")

def test_process_record_exists():
    """Verify the agent created the process_record.py script."""
    assert os.path.isfile("/home/user/process_record.py"), "The script /home/user/process_record.py is missing."

def generate_fuzz_inputs(n=500, seed=42):
    random.seed(seed)
    inputs = []

    def random_garbage(length):
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation.replace('{', '').replace('}', ''), k=length))

    for i in range(n):
        category = random.random()
        if category < 0.6:
            # Valid JSON with garbage
            valid_jsons = [
                '{"status": "ok"}',
                '{"value": 42, "data": [1, 2, 3]}',
                '{"empty": {}}',
                '{"nested": {"a": "b"}}'
            ]
            core = random.choice(valid_jsons)
            prefix = random_garbage(random.randint(0, 50))
            suffix = random_garbage(random.randint(0, 50))
            text = prefix + core + suffix
        elif category < 0.8:
            # Malformed JSON inside brackets
            core = '{"bad": json, "missing_quotes": true'
            prefix = random_garbage(random.randint(0, 50))
            suffix = random_garbage(random.randint(0, 50))
            text = prefix + core + '}' + suffix
        else:
            # No brackets
            text = random_garbage(random.randint(10, 100))

        hex_encoded = text.encode('utf-8').hex()
        inputs.append(hex_encoded)

    return inputs

def test_fuzz_equivalence():
    """Compare the agent's script against the oracle using 500 randomized inputs."""
    agent_script = "/home/user/process_record.py"
    oracle_script = "/app/oracle_processor.py"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script missing: {oracle_script}"

    inputs = generate_fuzz_inputs(n=500)

    for i, hex_input in enumerate(inputs):
        # Run Oracle
        oracle_cmd = [sys.executable, oracle_script, hex_input]
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        oracle_out = oracle_proc.stdout.strip()

        # Run Agent
        agent_cmd = [sys.executable, agent_script, hex_input]
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            error_msg = (
                f"Mismatch on fuzz input {i}!\n"
                f"Input (hex): {hex_input}\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output:  {agent_out}\n"
            )
            pytest.fail(error_msg)