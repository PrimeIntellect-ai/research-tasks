# test_final_state.py
import os
import subprocess
import random
import pytest

def test_all_configs_utf8_exists():
    utf8_path = "/home/user/all_configs.utf8"
    assert os.path.isfile(utf8_path), f"File {utf8_path} is missing."

    # We expect it to be valid UTF-8
    with open(utf8_path, "rb") as f:
        data = f.read()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail(f"File {utf8_path} is not valid UTF-8.")

    assert "key1=value1" in text, "Expected content from a.conf missing in all_configs.utf8"
    assert "résumé" in text, "Expected decoded content from a.conf missing in all_configs.utf8"
    assert "setting=enabled" in text, "Expected content from b.conf missing in all_configs.utf8"

def test_fuzz_equivalence():
    oracle_path = "/app/diff_encoder"
    agent_path = "/home/user/encoder"

    assert os.path.isfile(agent_path), f"Agent program missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program {agent_path} is not executable"

    random.seed(42)

    for i in range(500):
        length = random.randint(0, 2048)
        input_data = bytes(random.choices(range(256), k=length))

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input of length {length}"
        assert agent_proc.returncode == 0, f"Agent failed on input of length {length}"

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Mismatch on random input of length {length}.\n"
                f"Oracle output length: {len(oracle_proc.stdout)}\n"
                f"Agent output length: {len(agent_proc.stdout)}\n"
                f"Oracle output (first 32 bytes): {oracle_proc.stdout[:32].hex()}\n"
                f"Agent output (first 32 bytes): {agent_proc.stdout[:32].hex()}"
            )

def test_encoded_configs():
    utf8_path = "/home/user/all_configs.utf8"
    encoded_path = "/home/user/encoded_configs.dat"
    oracle_path = "/app/diff_encoder"

    assert os.path.isfile(utf8_path), f"{utf8_path} is missing"
    assert os.path.isfile(encoded_path), f"{encoded_path} is missing"

    with open(utf8_path, "rb") as f:
        utf8_data = f.read()

    with open(encoded_path, "rb") as f:
        encoded_data = f.read()

    oracle_proc = subprocess.run([oracle_path], input=utf8_data, capture_output=True)
    assert oracle_proc.returncode == 0, "Oracle failed to process all_configs.utf8"

    assert oracle_proc.stdout == encoded_data, (
        f"Contents of {encoded_path} do not match expected output from encoding {utf8_path}."
    )