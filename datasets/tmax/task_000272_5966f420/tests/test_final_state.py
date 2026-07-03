# test_final_state.py
import asyncio
import json
import subprocess
import tempfile
import re
import pytest
import websockets

@pytest.mark.asyncio
async def test_websocket_server_invalid_token():
    """Test that the server closes the connection with code 1008 for an invalid token."""
    uri = "ws://127.0.0.1:8081"
    try:
        async with websockets.connect(uri) as ws:
            payload = {"token": "wrong", "c_code": "int main(){}"}
            await ws.send(json.dumps(payload))
            try:
                await ws.recv()
                pytest.fail("Connection was not closed as expected.")
            except websockets.exceptions.ConnectionClosed as e:
                assert e.code == 1008, f"Expected close code 1008 for invalid token, got {e.code}"
    except ConnectionRefusedError:
        pytest.fail("Could not connect to WebSocket server on 127.0.0.1:8081.")

@pytest.mark.asyncio
async def test_websocket_server_valid_token():
    """Test that the server processes valid C code and returns the correct mov count."""
    c_code = "int main() { int a = 5; int b = a; return b; }"

    # Independently compute the expected mov count
    with tempfile.NamedTemporaryFile(suffix=".c", mode="w", delete=False) as f:
        f.write(c_code)
        temp_c = f.name

    temp_s = temp_c[:-2] + ".s"
    try:
        subprocess.run(
            ["aarch64-linux-gnu-gcc", "-S", "-O0", temp_c, "-o", temp_s],
            check=True,
            capture_output=True
        )
    except FileNotFoundError:
        pytest.fail("aarch64-linux-gnu-gcc is not installed or not in PATH.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile C code for truth generation: {e.stderr.decode()}")

    expected_count = 0
    with open(temp_s, "r") as f:
        for line in f:
            if re.search(r'(?i)\bmov\b', line):
                expected_count += 1

    uri = "ws://127.0.0.1:8081"
    try:
        async with websockets.connect(uri) as ws:
            payload = {"token": "omega-build-99", "c_code": c_code}
            await ws.send(json.dumps(payload))
            response = await ws.recv()
            data = json.loads(response)

            assert data.get("result") == "compiled", f"Expected result 'compiled', got {data.get('result')}"
            assert data.get("mov_count") == expected_count, f"Expected mov_count {expected_count}, got {data.get('mov_count')}"
    except ConnectionRefusedError:
        pytest.fail("Could not connect to WebSocket server on 127.0.0.1:8081.")
    except json.JSONDecodeError:
        pytest.fail(f"Server did not return valid JSON. Response: {response}")