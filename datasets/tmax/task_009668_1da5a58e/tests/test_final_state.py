# test_final_state.py

import os
import sqlite3
import re
import py_compile
import pytest

WORKSPACE_DIR = "/home/user/telemetry_system"
SERVER_FILE = os.path.join(WORKSPACE_DIR, "server.py")
DB_FILE = os.path.join(WORKSPACE_DIR, "db.sqlite3")
NGINX_CONF = os.path.join(WORKSPACE_DIR, "nginx.conf")
E2E_RESULT_LOG = os.path.join(WORKSPACE_DIR, "e2e_result.log")

def test_server_syntax_and_memory_leak_fixed():
    assert os.path.isfile(SERVER_FILE), f"File {SERVER_FILE} does not exist."

    # Check for syntax errors by compiling
    try:
        py_compile.compile(SERVER_FILE, doraise=True)
    except py_compile.PyCompileError as e:
        pytest.fail(f"Syntax error in {SERVER_FILE}: {e}")

    # Check for memory leak fix
    with open(SERVER_FILE, "r") as f:
        content = f.read()

    # Ensure unbounded list append is removed
    assert "message_history.append" not in content, "Memory leak still present: 'message_history.append' found in server.py."

def test_database_schema_migrated():
    assert os.path.isfile(DB_FILE), f"Database file {DB_FILE} does not exist."

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check if table was renamed
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='device_telemetry';")
    table = cursor.fetchone()
    assert table is not None, "Table 'device_telemetry' does not exist. Did you rename 'telemetry'?"

    # Check columns
    cursor.execute("PRAGMA table_info(device_telemetry);")
    columns = {row[1]: row[2] for row in cursor.fetchall()}

    assert "id" in columns, "Column 'id' missing in 'device_telemetry' table."
    assert "data" in columns, "Column 'data' missing in 'device_telemetry' table."
    assert "received_at" in columns, "Column 'received_at' missing in 'device_telemetry' table."
    assert "DATETIME" in columns["received_at"].upper(), "Column 'received_at' is not of type DATETIME."

    conn.close()

def test_nginx_configuration():
    assert os.path.isfile(NGINX_CONF), f"Nginx config {NGINX_CONF} does not exist."

    with open(NGINX_CONF, "r") as f:
        content = f.read().lower()

    # Check for WebSocket upgrade headers
    assert "proxy_set_header upgrade $http_upgrade;" in content or "proxy_set_header upgrade $http_upgrade" in content, "Nginx config missing 'proxy_set_header Upgrade $http_upgrade;'"
    assert "proxy_set_header connection" in content and "upgrade" in content, "Nginx config missing 'proxy_set_header Connection \"upgrade\";'"
    assert "9000" in content, "Nginx config does not seem to listen on port 9000."

def test_e2e_result_log():
    assert os.path.isfile(E2E_RESULT_LOG), f"E2E result log {E2E_RESULT_LOG} does not exist. Did the Node.js script run successfully?"

    with open(E2E_RESULT_LOG, "r") as f:
        content = f.read().strip()

    assert "E2E_PASS" in content, f"Expected 'E2E_PASS' in {E2E_RESULT_LOG}, but found '{content}'."