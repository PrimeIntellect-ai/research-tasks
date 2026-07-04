# test_final_state.py

import os
import subprocess
import random
import pytest

def test_flash_count():
    path = "/home/user/flash_count.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "42", f"Expected flash count to be 42, but got {content}"

def test_telemetry_raw_log_recovered():
    path = "/home/user/telemetry_raw.log"
    assert os.path.exists(path), f"File {path} does not exist."

    # Extract expected strings from the image
    img_path = "/app/drone_data.img"
    assert os.path.exists(img_path), f"Image {img_path} missing."

    try:
        strings_output = subprocess.check_output(["strings", img_path], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run strings on drone_data.img")

    expected_lines = [line.strip() for line in strings_output.splitlines() if "SEQ:" in line]

    with open(path, "r") as f:
        recovered_lines = [line.strip() for line in f.readlines() if line.strip()]

    for expected in expected_lines:
        assert expected in recovered_lines, f"Missing recovered line: {expected}"

def test_reconstruct_script_and_timeline():
    script_path = "/home/user/reconstruct.sh"
    timeline_path = "/home/user/timeline.log"

    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Run the script to generate timeline.log if it doesn't exist or just to test
    subprocess.run([script_path], check=True)

    assert os.path.exists(timeline_path), f"Timeline file {timeline_path} does not exist."

    with open(timeline_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Check if lines are sorted by SEQ ID
    seq_ids = []
    for line in lines:
        if "SEQ:" in line:
            seq_part = line.split("SEQ:")[1].split()[0]
            seq_ids.append(seq_part)

    assert seq_ids == sorted(seq_ids), "Timeline is not sorted chronologically by SEQ ID."

def test_decoder_fuzz_equivalence():
    oracle_path = "/opt/oracle_decoder"
    agent_path = "/home/user/fixed_decoder"

    assert os.path.exists(oracle_path), f"Oracle decoder missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent decoder missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent decoder {agent_path} is not executable."

    random.seed(42)
    charset = "0123456789ABCDEF"

    for _ in range(1000):
        test_input = "".join(random.choice(charset) for _ in range(16))

        try:
            oracle_proc = subprocess.run([oracle_path], input=test_input, text=True, capture_output=True, check=True)
            oracle_out = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {test_input}: {e.stderr}")

        try:
            agent_proc = subprocess.run([agent_path], input=test_input, text=True, capture_output=True, check=True)
            agent_out = agent_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input {test_input}: {e.stderr}")

        assert agent_out == oracle_out, f"Mismatch on input {test_input}. Oracle: {oracle_out}, Agent: {agent_out}"