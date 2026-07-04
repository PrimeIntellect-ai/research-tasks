# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_random_plate():
    pattern = random.choice(["[A-Z]{3}[0-9]{3}", "[A-Z]{2}[0-9]{4}", "UNKNOWN"])
    if pattern == "[A-Z]{3}[0-9]{3}":
        return "".join(random.choices(string.ascii_uppercase, k=3)) + "".join(random.choices(string.digits, k=3))
    elif pattern == "[A-Z]{2}[0-9]{4}":
        return "".join(random.choices(string.ascii_uppercase, k=2)) + "".join(random.choices(string.digits, k=4))
    else:
        return "UNKNOWN"

def generate_fuzz_input(num_lines):
    lines = []
    prev_line_data = None

    for _ in range(num_lines):
        if prev_line_data and random.random() < 0.3:
            epoch = prev_line_data['epoch'] + random.randint(0, 4000)
            event = prev_line_data['event']
            plate = prev_line_data['plate']
            speed = prev_line_data['speed']
        else:
            epoch = random.randint(1600000000000, 1600000500000)
            event = random.choice(["SPEEDING", "IDLE", "BRAKE", "CRASH"])
            plate = generate_random_plate()
            speed = random.randint(0, 120)

        lines.append(f"{epoch}|{event}|{plate}|{speed}")
        prev_line_data = {'epoch': epoch, 'event': event, 'plate': plate, 'speed': speed}

    return "\n".join(lines) + "\n"

def test_extracted_logs_exist():
    assert os.path.isfile('/home/user/extracted_logs.srt'), "Part 1 failed: /home/user/extracted_logs.srt does not exist."

def test_raw_telemetry_exists_and_content():
    raw_path = '/home/user/raw_telemetry.txt'
    assert os.path.isfile(raw_path), f"Part 1 failed: {raw_path} does not exist."

    with open(raw_path, 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) >= 4, "raw_telemetry.txt does not contain the expected number of lines."
    assert "1600000000000|SPEEDING|XYZ789|65" in content, "Expected telemetry line missing from raw_telemetry.txt"
    assert "1600000001500|SPEEDING|XYZ789|65" in content, "Expected telemetry line missing from raw_telemetry.txt"
    assert "1600000004000|BRAKE|ABC123|20" in content, "Expected telemetry line missing from raw_telemetry.txt"
    assert "1600000005000|BRAKE|A1B2C3|10" in content, "Expected telemetry line missing from raw_telemetry.txt"

def test_process_telemetry_executable():
    script_path = '/home/user/process_telemetry.sh'
    assert os.path.isfile(script_path), f"Part 2 failed: {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Part 2 failed: {script_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = '/app/oracle_etl.sh'
    agent_path = '/home/user/process_telemetry.sh'

    assert os.path.isfile(oracle_path), "Oracle script missing."
    assert os.path.isfile(agent_path), "Agent script missing."

    random.seed(42)
    N = 200

    for i in range(N):
        num_lines = random.randint(20, 500)
        input_data = generate_fuzz_input(num_lines)

        oracle_proc = subprocess.run([oracle_path], input=input_data, text=True, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, text=True, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"

        if oracle_proc.stdout != agent_proc.stdout:
            error_msg = (
                f"Mismatch found on fuzz iteration {i}.\n"
                f"Input:\n{input_data[:200]}...\n\n"
                f"Oracle Output (first 200 chars):\n{oracle_proc.stdout[:200]}...\n\n"
                f"Agent Output (first 200 chars):\n{agent_proc.stdout[:200]}...\n"
            )
            pytest.fail(error_msg)