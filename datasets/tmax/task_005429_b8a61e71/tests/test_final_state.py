# test_final_state.py

import os
import asyncio
import websockets
import pytest

def test_shared_library_compiled():
    assert os.path.isfile("/app/libtelemetry.so"), "Shared library /app/libtelemetry.so was not compiled."

@pytest.mark.asyncio
async def test_websocket_server_responses():
    uri = "ws://127.0.0.1:8765"

    try:
        async with websockets.connect(uri) as websocket:
            # Test valid command
            await websocket.send("GET_TELEMETRY")
            response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
            assert response == "SYSTEM_STABLE_ALL_GREEN", f"Expected 'SYSTEM_STABLE_ALL_GREEN', but got '{response}'"

            # Test invalid command
            await websocket.send("UNKNOWN_COMMAND")
            response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
            assert response == "INVALID_COMMAND", f"Expected 'INVALID_COMMAND', but got '{response}'"

    except ConnectionRefusedError:
        pytest.fail("WebSocket server is not running or not listening on 127.0.0.1:8765.")
    except asyncio.TimeoutError:
        pytest.fail("WebSocket server did not respond within the timeout period.")
    except Exception as e:
        pytest.fail(f"WebSocket communication failed with error: {e}")