# test_final_state.py

import os
import json
import re
import pytest

def test_emulator_proto_exists_and_valid():
    proto_path = "/home/user/emulator.proto"
    assert os.path.exists(proto_path), f"File {proto_path} does not exist."

    with open(proto_path, "r") as f:
        content = f.read()

    assert 'syntax = "proto3";' in content or "syntax='proto3';" in content.replace(" ", ""), "Missing proto3 syntax declaration."
    assert "package iot_test;" in content, "Missing package iot_test declaration."
    assert "service Emulator" in content, "Missing Emulator service."
    assert "rpc ExecuteFirmware" in content, "Missing ExecuteFirmware RPC."
    assert "message FirmwareRequest" in content, "Missing FirmwareRequest message."
    assert "message FirmwareResponse" in content, "Missing FirmwareResponse message."
    assert "bytes bytecode = 1;" in content, "FirmwareRequest missing bytes bytecode field."
    assert "repeated int32 readings = 1;" in content, "FirmwareResponse missing repeated int32 readings field."

def test_scripts_exist():
    server_path = "/home/user/server.py"
    client_path = "/home/user/client.py"

    assert os.path.exists(server_path), f"File {server_path} does not exist."
    assert os.path.exists(client_path), f"File {client_path} does not exist."

def test_results_json_correct():
    results_path = "/home/user/test_results.json"
    assert os.path.exists(results_path), f"File {results_path} does not exist. Did the client script run successfully?"

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} does not contain valid JSON.")

    expected_results = [20, 25, 20]
    assert results == expected_results, f"Expected {expected_results} in {results_path}, but got {results}."