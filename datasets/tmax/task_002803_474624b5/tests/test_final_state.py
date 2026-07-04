# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest

def test_config_env_fixed():
    config_path = "/app/bash-json-reshaper-1.1/config.env"
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    assert "ENABLE_UNICODE_DECODE=1" in content, f"Config file {config_path} was not fixed. Expected 'ENABLE_UNICODE_DECODE=1'."

def test_agent_script_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Agent script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Agent script {script_path} is not executable."

def generate_random_json_lines(num_lines):
    lines = []
    unicode_escapes = ["\\u00A0", "\\u2713", "\\u2022", "\\u2603", "\\u2728"]
    for _ in range(num_lines):
        id_val = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        num_metrics = random.randint(1, 5)
        metrics = {}
        for _ in range(num_metrics):
            m_name = "".join(random.choices(string.ascii_lowercase, k=5))
            m_val = random.randint(0, 1000)
            metrics[m_name] = m_val

        text_parts = []
        for _ in range(random.randint(1, 5)):
            text_parts.append("".join(random.choices(string.ascii_letters, k=5)))
            if random.random() < 0.5:
                text_parts.append(random.choice(unicode_escapes))

        text_val = " ".join(text_parts)

        # Build JSON manually to preserve literal unicode escapes without python escaping them
        # json.dumps will escape things, but we want literal \uXXXX in the string
        # text_val already has double backslash because of python string literal, so it becomes \uXXXX in JSON
        record = {
            "id": id_val,
            "metrics": metrics,
            "text": text_val
        }
        lines.append(json.dumps(record))
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/run_pipeline_oracle.sh"
    agent_path = "/home/user/run_pipeline.sh"

    assert os.path.isfile(oracle_path), f"Oracle script {oracle_path} missing."

    random.seed(42)

    for i in range(100):
        num_lines = random.randint(10, 100)
        input_data = generate_random_json_lines(num_lines)

        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        agent_proc = subprocess.run(
            [agent_path],
            input=input_data.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on iteration {i}. Agent: {agent_proc.returncode}, Oracle: {oracle_proc.returncode}"
        assert agent_proc.stdout == oracle_proc.stdout, f"Output mismatch on iteration {i}.\nInput:\n{input_data[:500]}...\n\nExpected:\n{oracle_proc.stdout.decode('utf-8')[:500]}...\n\nGot:\n{agent_proc.stdout.decode('utf-8')[:500]}..."