# test_final_state.py
import os
import json
import subprocess
import sys
import socket
import time

def test_server_listening():
    """Verify that a process is listening on 127.0.0.1:8765."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = s.connect_ex(('127.0.0.1', 8765))
        assert result == 0, "No process is listening on 127.0.0.1:8765."
    finally:
        s.close()

def test_websocket_logic_and_constraints():
    """
    Connects to the WebSocket server to test:
    1. Valid JSON handling.
    2. 1-to-1 worker-to-task constraint (no worker used twice).
    3. Correct 'unsatisfiable' error when constraints cannot be met.
    """
    script = """
import asyncio
import json
import sys

try:
    import websockets
except ImportError:
    print("websockets library is not installed in the environment.")
    sys.exit(1)

async def verify():
    try:
        async with websockets.connect("ws://127.0.0.1:8765") as ws:
            # Payload 1: Satisfiable, requires unique workers for the same skill
            await ws.send(json.dumps({
                "tasks": [{"id": "t1", "required_skill": "A"}, {"id": "t2", "required_skill": "A"}],
                "workers": [{"id": "w1", "skill": "A"}, {"id": "w2", "skill": "B"}, {"id": "w3", "skill": "A"}]
            }))
            resp1_raw = await ws.recv()
            try:
                resp1 = json.loads(resp1_raw)
            except json.JSONDecodeError:
                print(f"Response 1 is not valid JSON: {resp1_raw}")
                return False

            if "assignments" not in resp1: 
                print(f"Missing 'assignments' in response 1: {resp1}")
                return False

            workers_used = set(a["worker_id"] for a in resp1["assignments"])
            if len(workers_used) != 2: 
                print(f"Workers not unique or incorrect number of assignments: {resp1['assignments']}")
                return False

            # Payload 2: Unsatisfiable, not enough workers with skill A
            await ws.send(json.dumps({
                "tasks": [{"id": "t1", "required_skill": "A"}, {"id": "t2", "required_skill": "A"}],
                "workers": [{"id": "w1", "skill": "A"}, {"id": "w2", "skill": "B"}]
            }))
            resp2_raw = await ws.recv()
            try:
                resp2 = json.loads(resp2_raw)
            except json.JSONDecodeError:
                print(f"Response 2 is not valid JSON: {resp2_raw}")
                return False

            if resp2.get("error") != "unsatisfiable": 
                print(f"Did not return correct unsatisfiable error: {resp2}")
                return False

        return True
    except Exception as e:
        print(f"Exception during WebSocket communication: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(verify())
    sys.exit(0 if success else 1)
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, f"WebSocket logic test failed.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_scheduler_log_file():
    """Verify that the server logs responses to /home/user/scheduler_log.jsonl correctly."""
    log_path = "/home/user/scheduler_log.jsonl"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. Did you append to it?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 2, f"Log file should contain at least 2 JSON lines after testing, found {len(lines)}."

    # Validate that the last two lines are valid JSON objects (from our test payloads)
    try:
        log1 = json.loads(lines[-2])
        log2 = json.loads(lines[-1])
    except json.JSONDecodeError as e:
        assert False, f"Log file contains invalid JSON on the last two lines: {e}"

    assert "assignments" in log1 or "error" in log1, "Second-to-last log entry missing expected keys."
    assert "assignments" in log2 or "error" in log2, "Last log entry missing expected keys."