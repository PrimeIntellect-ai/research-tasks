# test_final_state.py

import os
import json
import asyncio
import pytest

def compute_expected_hash(filename):
    return sum(ord(c) for c in filename) % 256

@pytest.mark.asyncio
async def test_websocket_server_protocol():
    # We assume the agent installed `websockets` to implement the server/tests
    try:
        import websockets
    except ImportError:
        pytest.fail("websockets library is not installed, cannot test WebSocket server.")

    uri = "ws://127.0.0.1:8765"

    try:
        async with websockets.connect(uri, ping_timeout=5) as websocket:
            # 1. Send auth message
            auth_msg = {"type": "auth", "token": "X7B9K2M4P1Q8"}
            await websocket.send(json.dumps(auth_msg))

            # Allow a tiny bit of time to ensure connection isn't closed
            await asyncio.sleep(0.5)
            assert websocket.open, "WebSocket connection was closed after sending correct auth token."

            # 2. Send organize message
            input_files = ["zebra.log", "alpha.txt", "beta.doc"]
            organize_msg = {
                "type": "organize",
                "files": input_files
            }
            await websocket.send(json.dumps(organize_msg))

            # 3. Wait for response
            response_str = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            response = json.loads(response_str)

            assert response.get("type") == "result", f"Expected response type 'result', got: {response.get('type')}"

            expected_sorted = sorted(input_files)
            assert response.get("sorted_files") == expected_sorted, f"Expected sorted files {expected_sorted}, got {response.get('sorted_files')}"

            expected_hashes = [compute_expected_hash(f) for f in expected_sorted]
            assert response.get("hashes") == expected_hashes, f"Expected hashes {expected_hashes}, got {response.get('hashes')}"

    except ConnectionRefusedError:
        pytest.fail("Connection refused. The WebSocket server is not running on 127.0.0.1:8765.")
    except asyncio.TimeoutError:
        pytest.fail("Timed out waiting for a response from the WebSocket server.")

def test_agent_files_exist():
    assert os.path.isfile("/home/user/server.py"), "Server script /home/user/server.py is missing."
    assert os.path.isfile("/home/user/tests/test_server.py"), "Test script /home/user/tests/test_server.py is missing."

    # Check if a shared library was compiled
    lib_dir = "/home/user/legacy_lib"
    so_files = [f for f in os.listdir(lib_dir) if f.endswith(".so")]
    assert len(so_files) > 0, "No compiled shared library (.so) found in /home/user/legacy_lib/"