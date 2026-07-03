# test_final_state.py

import os
import subprocess
import random
import pytest

def test_iot_sender_fixed():
    """Test that the IoT sender package typo is fixed and it detects the environment variable."""
    sender_path = "/app/iot-sender-1.2.0/sender.py"
    assert os.path.exists(sender_path), f"Sender script missing at {sender_path}"

    env = os.environ.copy()
    env["IOT_ENDPOINT"] = "http://diagnostic.local"

    result = subprocess.run(
        ["python3", sender_path],
        env=env,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Sender script failed with return code {result.returncode}. Stderr: {result.stderr}"
    assert "Endpoint configured: http://diagnostic.local" in result.stdout, \
        f"Sender script did not print the expected success message. Output: {result.stdout}"

def test_fstab_configured():
    """Test that the fstab file is correctly configured."""
    fstab_path = "/home/user/device_fstab"
    assert os.path.exists(fstab_path), f"fstab file missing at {fstab_path}"

    with open(fstab_path, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    assert len(lines) == 1, f"Expected exactly one non-empty line in {fstab_path}, found {len(lines)}"

    fields = lines[0].split()
    assert len(fields) == 6, f"Expected 6 fields in fstab line, found {len(fields)}. Line: {lines[0]}"

    assert fields[0] == "UUID=1234-ABCD", f"Expected UUID=1234-ABCD, got {fields[0]}"
    assert fields[1] == "/home/user/sensor_data", f"Expected mount point /home/user/sensor_data, got {fields[1]}"
    assert fields[2] == "ext4", f"Expected filesystem ext4, got {fields[2]}"
    assert fields[3] == "defaults,ro,noauto,user", f"Expected options defaults,ro,noauto,user, got {fields[3]}"
    assert fields[4] == "0", f"Expected dump value 0, got {fields[4]}"
    assert fields[5] == "0", f"Expected pass value 0, got {fields[5]}"

def generate_valid_frame(length):
    magic = 0x5A
    sensor_id = random.randint(0, 255)
    payload = [random.randint(0, 255) for _ in range(length)]

    frame = [magic, sensor_id, length] + payload
    checksum = 0
    for b in frame:
        checksum ^= b
    frame.append(checksum)

    return bytes(frame).hex()

def generate_fuzz_inputs(n=2000):
    random.seed(42)
    inputs = []

    # 40% valid frames
    for _ in range(int(n * 0.4)):
        inputs.append(generate_valid_frame(random.randint(0, 200)))

    # 15% invalid hex
    for _ in range(int(n * 0.15)):
        valid = generate_valid_frame(random.randint(0, 50))
        if len(valid) > 0:
            idx = random.randint(0, len(valid) - 1)
            char_to_insert = random.choice("GHIJKLMNOPQRSTUVWXYZ")
            inputs.append(valid[:idx] + char_to_insert + valid[idx+1:])
        else:
            inputs.append("X")

    # 15% incorrect lengths
    for _ in range(int(n * 0.15)):
        valid = generate_valid_frame(random.randint(0, 50))
        if random.choice([True, False]) and len(valid) >= 2:
            inputs.append(valid[:-2])  # truncated
        else:
            inputs.append(valid + "00")  # extra byte

    # 15% incorrect magic
    for _ in range(int(n * 0.15)):
        length = random.randint(0, 50)
        sensor_id = random.randint(0, 255)
        payload = [random.randint(0, 255) for _ in range(length)]
        magic = random.choice([m for m in range(256) if m != 0x5A])
        frame = [magic, sensor_id, length] + payload
        checksum = 0
        for b in frame:
            checksum ^= b
        frame.append(checksum)
        inputs.append(bytes(frame).hex())

    # 15% incorrect checksum
    for _ in range(int(n * 0.15)):
        valid = generate_valid_frame(random.randint(0, 50))
        if len(valid) >= 2:
            b = int(valid[-2:], 16)
            b ^= random.randint(1, 255)
            inputs.append(valid[:-2] + f"{b:02x}")
        else:
            inputs.append("00")

    # Fill remaining to exact N
    while len(inputs) < n:
        inputs.append(generate_valid_frame(random.randint(0, 50)))

    random.shuffle(inputs)
    return inputs[:n]

def test_telemetry_parser_fuzz_equivalence():
    """Test that the agent's telemetry parser behaves identically to the oracle."""
    oracle_path = "/app/telemetry_oracle"
    agent_path = "/home/user/parse_telemetry.py"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent script missing at {agent_path}"

    inputs = generate_fuzz_inputs(2000)

    for hex_input in inputs:
        # Run oracle
        oracle_res = subprocess.run(
            [oracle_path, hex_input],
            capture_output=True,
            text=True
        )
        oracle_output = oracle_res.stdout.strip()

        # Run agent
        agent_res = subprocess.run(
            ["python3", agent_path, hex_input],
            capture_output=True,
            text=True
        )
        agent_output = agent_res.stdout.strip()

        assert agent_output == oracle_output, (
            f"Output mismatch on input: {hex_input}\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output:  {agent_output}\n"
            f"Agent stderr:  {agent_res.stderr.strip()}"
        )