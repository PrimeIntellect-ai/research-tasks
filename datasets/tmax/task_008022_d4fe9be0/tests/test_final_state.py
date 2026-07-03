# test_final_state.py
import os
import struct
import pytest

def test_result_variance():
    wal_path = "/home/user/wal.dat"
    assert os.path.exists(wal_path), f"{wal_path} is missing."

    # Derive the expected truth dynamically from the WAL file
    values = []
    with open(wal_path, "rb") as f:
        while True:
            chunk = f.read(12)
            if len(chunk) < 12:
                # Ignore incomplete trailing records as per the task requirements
                break
            _, val = struct.unpack("<Id", chunk)
            values.append(val)

    assert len(values) > 0, "No valid records found in WAL."

    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    expected_output = f"{variance:.6f}"

    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"{result_path} is missing. The service may not have run or failed to write output."

    with open(result_path, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"Variance mismatch. Expected {expected_output}, but got '{actual_output}'."

def test_cargo_toml_fixed():
    cargo_toml_path = "/home/user/wal_processor/Cargo.toml"
    assert os.path.exists(cargo_toml_path), f"{cargo_toml_path} is missing."
    with open(cargo_toml_path, "r") as f:
        content = f.read()
    assert "=1.0.9999" not in content, "Cargo.toml still contains the invalid 'anyhow' dependency version."

def test_cargo_config_fixed():
    config_path = "/home/user/wal_processor/.cargo/config.toml"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            content = f.read()
        assert "--invalid-flag-that-breaks-build" not in content, "The .cargo/config.toml file still contains the invalid rustflag."