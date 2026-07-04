# test_final_state.py
import os
import time
import json
import asyncio
import pytest
import numpy as np
import pandas as pd
import websockets

@pytest.mark.asyncio
async def test_rate_limiting():
    """Test that rate limiting closes the connection with code 4000."""
    uri = "ws://127.0.0.1:8080"

    async def blast_requests():
        try:
            async with websockets.connect(uri) as ws:
                for _ in range(15):
                    payload = json.dumps({"action": "compute", "window": 3, "data": [1.0, 2.0, 3.0]})
                    await ws.send(payload)

                # Now try to recv, expecting a ConnectionClosed with code 4000
                for _ in range(15):
                    await ws.recv()
        except websockets.exceptions.ConnectionClosed as e:
            return e.code
        except Exception:
            return None
        return None

    code = await blast_requests()
    assert code == 4000, f"Expected WebSocket to be closed with code 4000 due to rate limiting, got {code}"

@pytest.mark.asyncio
async def test_correctness_and_latency():
    """Test the correctness (MSE) and latency of the compute endpoint."""
    # Wait for the rate limit window to reset from the previous test
    await asyncio.sleep(1.1)

    uri = "ws://127.0.0.1:8080"
    window = 100
    np.random.seed(42)
    data = np.random.rand(50000).tolist()

    # Calculate golden result using pandas
    s = pd.Series(data)
    golden = s.rolling(window).median().fillna(0.0).values

    payload = json.dumps({"action": "compute", "window": window, "data": data})

    async def measure():
        async with websockets.connect(uri) as ws:
            start = time.time()
            await ws.send(payload)
            resp = await ws.recv()
            latency = time.time() - start
            return resp, latency

    try:
        resp_str, latency = await measure()
    except Exception as e:
        pytest.fail(f"Failed to connect and measure latency: {e}")

    try:
        resp_data = json.loads(resp_str)
    except json.JSONDecodeError:
        pytest.fail("Server did not return valid JSON.")

    assert "result" in resp_data, "Response JSON must contain a 'result' key"

    result = np.array(resp_data["result"])
    assert len(result) == len(data), f"Result length ({len(result)}) must match input length ({len(data)})"

    mse = np.mean((result - golden) ** 2)
    assert mse < 1e-5, f"Mean Squared Error is too high: {mse} >= 1e-5. Implementation is incorrect."

    assert latency <= 0.15, f"Latency metric failed: {latency:.4f} > 0.15 seconds. Implementation is too slow."

def test_files_exist():
    """Verify that the required C files were created."""
    assert os.path.exists("/app/math_lib.c"), "/app/math_lib.c is missing."
    assert os.path.exists("/app/libmath.so"), "/app/libmath.so is missing."
    assert os.path.exists("/app/ws_server.py"), "/app/ws_server.py is missing."