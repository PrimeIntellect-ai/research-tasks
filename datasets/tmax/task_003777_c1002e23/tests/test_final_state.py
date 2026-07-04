# test_final_state.py

import os
import json
import math
import asyncio
import pytest

def test_libcore_so_exists():
    assert os.path.isfile("/app/libcore.so"), "/app/libcore.so is missing. The C library was not compiled."

def test_run_sh_exists_and_executable():
    assert os.path.isfile("/app/run.sh"), "/app/run.sh is missing."
    assert os.access("/app/run.sh", os.X_OK), "/app/run.sh is not executable."

@pytest.mark.asyncio
async def test_websocket_server():
    # We expect the agent to have installed the websockets library as suggested in the prompt.
    try:
        import websockets
    except ImportError:
        pytest.fail("The 'websockets' library is not installed. It is required to test the WebSocket server.")

    uri = "ws://127.0.0.1:8765"

    # Calculate the expected result
    a, b, c = 7, 22, 81
    x = 1.5
    expected_result = (a * math.sin(x)) + (b * math.cos(x)) + (c * math.exp(-x))

    try:
        async with websockets.connect(uri, ping_timeout=5) as websocket:
            # Test valid token
            request = {"token": "7_22_81", "x": x}
            await websocket.send(json.dumps(request))

            response_str = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            response = json.loads(response_str)

            assert "result" in response, f"Expected 'result' in response, got: {response}"
            actual_result = response["result"]

            assert math.isclose(actual_result, expected_result, rel_tol=1e-5), \
                f"Expected result approx {expected_result}, got {actual_result}"

    except ConnectionRefusedError:
        pytest.fail("Could not connect to WebSocket server at 127.0.0.1:8765. Is it running?")
    except asyncio.TimeoutError:
        pytest.fail("WebSocket server did not respond within the timeout.")
    except Exception as e:
        pytest.fail(f"WebSocket communication failed: {e}")

@pytest.mark.asyncio
async def test_websocket_server_invalid_token():
    try:
        import websockets
    except ImportError:
        pytest.skip("websockets library not available")

    uri = "ws://127.0.0.1:8765"

    try:
        async with websockets.connect(uri, ping_timeout=5) as websocket:
            request = {"token": "wrong_token", "x": 1.5}
            await websocket.send(json.dumps(request))

            try:
                response_str = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                # If it responds, it should be an error
                try:
                    response = json.loads(response_str)
                    assert "result" not in response, "Server returned a result for an invalid token instead of dropping or erroring."
                except json.JSONDecodeError:
                    pass # Non-JSON error response is acceptable
            except websockets.exceptions.ConnectionClosed:
                # Dropping connection is acceptable
                pass
            except asyncio.TimeoutError:
                # No response (dropped) is acceptable
                pass
    except ConnectionRefusedError:
        pytest.fail("Could not connect to WebSocket server at 127.0.0.1:8765.")