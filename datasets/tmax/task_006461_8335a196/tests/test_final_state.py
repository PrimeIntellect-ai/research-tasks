# test_final_state.py
import os
import json
import subprocess
import time
import sys
import tempfile
import pytest

def test_result_json():
    result_path = '/home/user/result.json'
    assert os.path.exists(result_path), f"{result_path} does not exist."
    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{result_path} does not contain valid JSON.")

    expected = ["libfront.so", "libmiddle_b.so", "libbase.so"]
    assert data == expected, f"Expected {expected} in result.json, got {data}"

def test_student_unittests():
    test_file = '/home/user/test_analyzer.py'
    assert os.path.exists(test_file), f"Unit test file {test_file} does not exist."

    # Run the student's test suite
    result = subprocess.run(
        [sys.executable, '-m', 'unittest', test_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Student's unit tests failed:\n{result.stderr}\n{result.stdout}"

def test_websocket_server():
    server_file = '/home/user/server.py'
    assert os.path.exists(server_file), f"Server file {server_file} does not exist."

    # Client script to test the websocket server
    client_script = """
import asyncio
import websockets
import json
import sys

async def test_ws():
    try:
        async with websockets.connect("ws://localhost:8765") as websocket:
            await websocket.send(json.dumps({"start": "libfront.so", "target": "libbase.so"}))
            response = await websocket.recv()
            data = json.loads(response)
            if data.get("path") == ["libfront.so", "libmiddle_b.so", "libbase.so"]:
                sys.exit(0)
            else:
                print(f"Wrong response: {data}")
                sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(2)

asyncio.run(test_ws())
"""

    # Start the server
    server_process = subprocess.Popen(
        [sys.executable, server_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Give the server a moment to start
        time.sleep(1.5)

        # Check if server crashed immediately
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            pytest.fail(f"Server crashed on startup. Return code: {server_process.returncode}\nStderr: {stderr.decode()}")

        # Run the client
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(client_script)
            client_file = f.name

        try:
            client_result = subprocess.run(
                [sys.executable, client_file],
                capture_output=True,
                text=True,
                timeout=5
            )
            assert client_result.returncode == 0, f"WebSocket client test failed. RC: {client_result.returncode}\nOutput: {client_result.stdout}\n{client_result.stderr}"
        finally:
            os.remove(client_file)

    finally:
        server_process.terminate()
        try:
            server_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server_process.kill()