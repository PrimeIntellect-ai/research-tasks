# test_final_state.py
import os
import subprocess
import sqlite3
import threading
import json
import time
import socket
import pytest

SCRIPT_PATH = "/home/user/secure_deploy.sh"
VERIFIER_DIR = "/home/user/verifier"
VERIFIER_BIN = "/home/user/verifier/verifier"
DB_PATH = "/home/user/deploy.db"
VALGRIND_LOG = "/home/user/valgrind.log"
WS_RESPONSE_FILE = "/home/user/ws_response.txt"

def dummy_websocket_server(host, port, received_messages, stop_event):
    import asyncio
    import websockets

    async def handler(websocket, path):
        try:
            async for message in websocket:
                received_messages.append(message)
                await websocket.send('{"status": "ok"}')
        except websockets.exceptions.ConnectionClosed:
            pass

    async def main():
        server = await websockets.serve(handler, host, port)
        await stop_event.wait()
        server.close()
        await server.wait_closed()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

@pytest.fixture(scope="module")
def run_script():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

    # Start dummy websocket server
    received_messages = []
    import asyncio
    stop_event = asyncio.Event()

    # We need a thread to run the asyncio loop
    def run_loop():
        dummy_websocket_server("127.0.0.1", 8765, received_messages, stop_event)

    ws_thread = threading.Thread(target=run_loop, daemon=True)
    ws_thread.start()

    # Wait for server to start
    time.sleep(1)

    try:
        result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True, timeout=30)
        yield result, received_messages
    finally:
        # Stop the server
        def stop():
            stop_event.set()

        # We can't easily set the asyncio event from another thread safely without loop.call_soon_threadsafe
        # But for this simple test, the daemon thread will just die when pytest exits.
        pass

def test_script_execution(run_script):
    result, _ = run_script
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

def test_verifier_compiled(run_script):
    assert os.path.isfile(VERIFIER_BIN), "Verifier binary was not compiled."
    assert os.access(VERIFIER_BIN, os.X_OK), "Verifier binary is not executable."

def test_sqlite_schema_migrated(run_script):
    assert os.path.isfile(DB_PATH), f"Database {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(releases);")
    columns = {col[1]: col[2] for col in cursor.fetchall()}
    conn.close()

    assert "is_secure" in columns, "Column 'is_secure' was not added to the 'releases' table."
    assert "INTEGER" in columns["is_secure"].upper(), "Column 'is_secure' is not of type INTEGER."

def test_valgrind_log_exists(run_script):
    assert os.path.isfile(VALGRIND_LOG), f"Valgrind log {VALGRIND_LOG} is missing."
    with open(VALGRIND_LOG, "r") as f:
        content = f.read()
        assert "Memcheck" in content or "valgrind" in content.lower(), "Valgrind log does not contain expected valgrind output."

def test_websocket_message_sent(run_script):
    _, received_messages = run_script
    assert len(received_messages) > 0, "No WebSocket messages were received by the server."

    last_msg = received_messages[-1]
    try:
        payload = json.loads(last_msg)
    except json.JSONDecodeError:
        pytest.fail(f"Received message is not valid JSON: {last_msg}")

    assert payload.get("status") == "ready", "JSON payload 'status' is not 'ready'."
    assert payload.get("pin") == 1337, f"JSON payload 'pin' is incorrect. Expected 1337, got {payload.get('pin')}."
    assert payload.get("leaks_checked") is True, "JSON payload 'leaks_checked' is not true."