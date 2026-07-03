# test_final_state.py

import os
import json
import pytest
import subprocess

BUILD_ENV_DIR = "/home/user/build_env"
COLLATZ_EXEC = os.path.join(BUILD_ENV_DIR, "collatz")
WS_HANDLER = os.path.join(BUILD_ENV_DIR, "ws_handler.py")
WS_PAYLOAD = os.path.join(BUILD_ENV_DIR, "ws_payload.json")

def collatz_length(n):
    steps = 0
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def test_executable_exists():
    """Check if the collatz executable was built and is executable."""
    assert os.path.isfile(COLLATZ_EXEC), f"Executable not found at {COLLATZ_EXEC}"
    assert os.access(COLLATZ_EXEC, os.X_OK), f"File at {COLLATZ_EXEC} is not executable"

def test_python_script_exists():
    """Check if the ws_handler.py script exists."""
    assert os.path.isfile(WS_HANDLER), f"Python script not found at {WS_HANDLER}"

def test_json_payload_exists_and_correct():
    """Check if ws_payload.json exists and has the correct schema and values."""
    assert os.path.isfile(WS_PAYLOAD), f"JSON payload not found at {WS_PAYLOAD}"

    with open(WS_PAYLOAD, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{WS_PAYLOAD} does not contain valid JSON")

    assert "channel" in data, "Key 'channel' missing from JSON payload"
    assert data["channel"] == "math_ws", f"Expected channel 'math_ws', got '{data['channel']}'"

    assert "message" in data, "Key 'message' missing from JSON payload"
    message = data["message"]

    assert "type" in message, "Key 'type' missing from message object"
    assert message["type"] == "collatz_len", f"Expected type 'collatz_len', got '{message['type']}'"

    assert "start_val" in message, "Key 'start_val' missing from message object"
    assert message["start_val"] == 837799, f"Expected start_val 837799, got {message['start_val']}"

    assert "steps" in message, "Key 'steps' missing from message object"

    expected_steps = collatz_length(837799)
    assert message["steps"] == expected_steps, f"Expected steps {expected_steps}, got {message['steps']}"