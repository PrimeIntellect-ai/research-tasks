# test_final_state.py

import os
import subprocess
import json
import math

def test_fixed_binary_success_rate():
    binary_path = "/home/user/telemetry_parser_fixed"
    assert os.path.isfile(binary_path), f"Fixed binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Fixed binary is not executable at {binary_path}"

    # Generate test inputs
    inputs = []

    # 50 Benign inputs
    for i in range(50):
        inputs.append(f"[DEBUG] BenignMessage{i} {float(i*i)}\n")
        inputs.append(f"[INFO] Some info message {i}\n")

    # 50 Malicious inputs (buffer overflow trigger)
    for i in range(50):
        long_msg = "A" * 200 + str(i)
        inputs.append(f"[DEBUG] {long_msg} 16.0\n")

    input_data = "".join(inputs)

    process = subprocess.Popen(
        [binary_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=input_data)

    # If it crashes with a segfault, returncode will be negative (e.g., -11)
    crashed = process.returncode != 0

    # Calculate success rate based on whether it crashed
    # In a real scenario, we'd also parse the output to ensure correctness,
    # but the primary metric threshold is avoiding the crash while processing.
    success_rate = 0.0 if crashed else 1.0

    assert success_rate >= 1.0, f"Expected success_rate >= 1.0, got {success_rate}. The binary crashed or returned non-zero exit code: {process.returncode}."

    # Validate that benign inputs were parsed correctly
    output_lines = [line for line in stdout.strip().split('\n') if line]

    # Check at least one benign output to ensure the core logic wasn't stubbed out
    found_benign = False
    for line in output_lines:
        try:
            data = json.loads(line)
            if data.get("level") == "DEBUG" and data.get("msg") == "BenignMessage4":
                assert math.isclose(data.get("val", 0), 4.0), "Square root calculation is incorrect"
                found_benign = True
                break
        except json.JSONDecodeError:
            continue

    assert found_benign, "The patched binary did not correctly output JSON for benign inputs."