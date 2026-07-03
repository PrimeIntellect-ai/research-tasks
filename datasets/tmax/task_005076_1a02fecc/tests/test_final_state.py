# test_final_state.py

import os
import json
import zlib
import base64
import asyncio
import pytest

try:
    import websockets
except ImportError:
    websockets = None

def get_expected_checksum(data: bytes) -> str:
    crc = zlib.crc32(data) & 0xFFFFFFFF
    final = crc ^ 0xDEADBEEF
    return f"{final:08x}"

def test_hypothesis_file_exists():
    path = "/home/user/test_checksum.py"
    assert os.path.isfile(path), f"Property-based test file {path} does not exist"
    with open(path, "r") as f:
        content = f.read()
    assert "hypothesis" in content, f"{path} does not seem to import or use 'hypothesis'"

def test_websocket_server_behavior():
    if websockets is None:
        pytest.fail("The 'websockets' library is not installed in the test environment.")

    async def run_ws_test():
        uri = "ws://127.0.0.1:8765/telemetry"

        test_cases = [
            (1, b"Hello World"),
            (42, b"Telemetry Data 123!@#"),
            (99, b""),
            (100, os.urandom(64))
        ]

        try:
            async with websockets.connect(uri) as websocket:
                for req_id, data in test_cases:
                    b64_data = base64.b64encode(data).decode('utf-8')
                    req = {"id": req_id, "data": b64_data}
                    await websocket.send(json.dumps(req))

                    try:
                        response_str = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                    except asyncio.TimeoutError:
                        pytest.fail(f"Timeout waiting for response to message id {req_id}")

                    try:
                        response = json.loads(response_str)
                    except json.JSONDecodeError:
                        pytest.fail(f"Server returned invalid JSON: {response_str}")

                    assert response.get("id") == req_id, f"Expected id {req_id}, got {response.get('id')}"
                    assert response.get("status") == "ack", f"Expected status 'ack', got {response.get('status')}"

                    expected_checksum = get_expected_checksum(data)
                    actual_checksum = response.get("checksum")
                    assert actual_checksum == expected_checksum, (
                        f"Checksum mismatch for data {data!r}. "
                        f"Expected {expected_checksum}, got {actual_checksum}"
                    )
        except ConnectionRefusedError:
            pytest.fail("Connection refused. The WebSocket server is not running or not listening on 127.0.0.1:8765.")
        except websockets.exceptions.InvalidURI:
            pytest.fail("Invalid WebSocket URI.")
        except Exception as e:
            pytest.fail(f"WebSocket client encountered an error: {e}")

    asyncio.run(run_ws_test())