# test_final_state.py

import os
import ctypes
import subprocess
import time
import sys
import pytest

def test_libalgo_exists_and_works():
    so_path = "/home/user/project/libalgo.so"
    assert os.path.exists(so_path), f"{so_path} does not exist. Did you modify the Makefile and run make?"

    try:
        lib = ctypes.CDLL(so_path)
    except Exception as e:
        pytest.fail(f"Failed to load {so_path} as a shared library: {e}")

    try:
        lib.compute_root.argtypes = [ctypes.c_double]
        lib.compute_root.restype = ctypes.c_double
    except AttributeError:
        pytest.fail("Function 'compute_root' is not exported by the shared library.")

    result = lib.compute_root(81.0)
    assert abs(result - 9.0) < 1e-5, f"compute_root(81.0) returned {result}, expected ~9.0"

def test_ws_server_behavior():
    server_script = "/home/user/project/ws_server.py"
    log_file = "/home/user/project/server_ready.log"

    assert os.path.exists(server_script), f"{server_script} does not exist."

    if os.path.exists(log_file):
        os.remove(log_file)

    # Start the WebSocket server in the background
    proc = subprocess.Popen([sys.executable, server_script])

    try:
        # Wait for the server to indicate it is ready
        ready = False
        for _ in range(50):
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    if "SERVER READY" in f.read():
                        ready = True
                        break
            time.sleep(0.1)

        assert ready, "Server did not write 'SERVER READY' to /home/user/project/server_ready.log within 5 seconds."

        # Test the WebSocket server using a small inline client script
        # This avoids directly importing the third-party 'websockets' library in the pytest process
        client_code = """
import asyncio
import websockets
import sys

async def run_client():
    try:
        async with websockets.connect("ws://localhost:8765") as ws:
            await ws.send("81.0")
            resp = await ws.recv()
            if abs(float(resp) - 9.0) < 1e-5:
                print("SUCCESS")
            else:
                print(f"WRONG_RESULT:{resp}")
    except Exception as e:
        print(f"ERROR:{e}")

asyncio.run(run_client())
"""
        client_proc = subprocess.run(
            [sys.executable, "-c", client_code],
            capture_output=True,
            text=True,
            timeout=5
        )

        output = client_proc.stdout.strip()
        assert "SUCCESS" in output, f"WebSocket client test failed. Output: {output} | Error: {client_proc.stderr}"

    finally:
        # Ensure the server process is cleaned up
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()