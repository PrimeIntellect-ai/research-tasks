# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_vendored_lib_built():
    assert os.path.isfile("/app/vendored/tiny-json-lines/libtinyjson.a"), "libtinyjson.a was not built."

def test_makefile_exists():
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), "Makefile does not exist in /home/user."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "build:" in content, "Makefile missing 'build' target."
    assert "run:" in content, "Makefile missing 'run' target."

def test_agent_binary_exists():
    assert os.path.isfile("/home/user/mask_loc"), "mask_loc binary was not compiled."
    assert os.access("/home/user/mask_loc", os.X_OK), "mask_loc is not executable."

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/mask_loc_oracle"
    agent_path = "/home/user/mask_loc"

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} not found."
    assert os.path.isfile(agent_path), f"Agent binary {agent_path} not found."

    random.seed(42)

    def generate_random_unicode_string():
        chars = []
        for _ in range(random.randint(5, 20)):
            if random.random() < 0.5:
                # ASCII
                chars.append(chr(random.randint(32, 126)))
            else:
                # Unicode character (will be escaped by json.dumps with ensure_ascii=True)
                # Avoid surrogates directly in python strings if possible, or use valid ranges
                chars.append(chr(random.randint(0x00A0, 0x27FF)))
        return "".join(chars).replace('"', '').replace('\\', '')

    for i in range(1000):
        obj = {
            "loc_key": generate_random_unicode_string(),
            "text": generate_random_unicode_string(),
            "user_id": random.randint(0, 2**64 - 1),
            "confidence_score": random.random()
        }

        # Ensure ascii to generate \uXXXX escapes
        input_json = json.dumps(obj, ensure_ascii=True)

        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_json,
            text=True,
            capture_output=True
        )

        agent_proc = subprocess.run(
            [agent_path],
            input=input_json,
            text=True,
            capture_output=True
        )

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {input_json}"

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent binary crashed or failed on input:\n{input_json}\nError:\n{agent_proc.stderr}")

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on input:\n{input_json}\n"
                f"Oracle output:\n{oracle_out}\n"
                f"Agent output:\n{agent_out}"
            )