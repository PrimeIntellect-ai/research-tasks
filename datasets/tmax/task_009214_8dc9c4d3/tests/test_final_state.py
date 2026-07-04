# test_final_state.py

import os
import json
import math
import subprocess
import pytest

def test_libsensor_so_exists():
    path = "/home/user/sensor_sim/libsensor.so"
    assert os.path.isfile(path), f"Shared library {path} does not exist. Did you run make?"

def test_libsensor_so_is_valid_elf():
    path = "/home/user/sensor_sim/libsensor.so"
    # Basic check to ensure it's a dynamically linked shared object
    try:
        output = subprocess.check_output(["file", path]).decode("utf-8")
        assert "shared object" in output, f"{path} is not a valid shared object. Output: {output}"
    except FileNotFoundError:
        pass # `file` command might not be available, skip this check if so

def test_processed_outputs_exists():
    path = "/home/user/sensor_sim/processed_outputs.jsonl"
    assert os.path.isfile(path), f"Output file {path} does not exist."

def test_processed_outputs_content():
    input_path = "/home/user/sensor_sim/requests.jsonl"
    output_path = "/home/user/sensor_sim/processed_outputs.jsonl"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(input_path, "r") as f:
        inputs = [json.loads(line.strip()) for line in f if line.strip()]

    with open(output_path, "r") as f:
        outputs = [json.loads(line.strip()) for line in f if line.strip()]

    assert len(outputs) == len(inputs), f"Expected {len(inputs)} lines in output, got {len(outputs)}."

    for in_obj, out_obj in zip(inputs, outputs):
        assert "id" in out_obj, f"Output object missing 'id': {out_obj}"
        assert out_obj["id"] == in_obj["id"], f"Expected id {in_obj['id']}, got {out_obj.get('id')}"

        is_active = in_obj.get("status") == "active"
        value = in_obj.get("value", 0)
        is_valid = is_active and (isinstance(value, (int, float)) and value > 0)

        if is_valid:
            assert "checksum" in out_obj, f"Expected valid request to have 'checksum', got: {out_obj}"
            assert "error" not in out_obj, f"Valid request should not have 'error', got: {out_obj}"

            # Compute expected checksum
            scaled = value * 100.0
            transformed = math.pow(scaled, 1.5)
            integer_part = int(transformed)
            expected_checksum = integer_part % 997

            assert out_obj["checksum"] == expected_checksum, (
                f"For id {in_obj['id']} (value={value}), expected checksum {expected_checksum}, "
                f"got {out_obj['checksum']}"
            )
        else:
            assert "error" in out_obj, f"Expected invalid request to have 'error', got: {out_obj}"
            assert "checksum" not in out_obj, f"Invalid request should not have 'checksum', got: {out_obj}"
            assert out_obj["error"] == "invalid_request", (
                f"For id {in_obj['id']}, expected error 'invalid_request', got '{out_obj['error']}'"
            )