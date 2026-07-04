# test_final_state.py

import os
import sys
import sqlite3
import subprocess
import pytest

def test_pyproject_toml_fixed():
    path = "/home/user/math-ws-proxy/pyproject.toml"
    assert os.path.isfile(path), "pyproject.toml does not exist"

    with open(path, "r") as f:
        content = f.read()

    assert "websockets" in content, "The 'websockets' dependency is missing from pyproject.toml"

def test_solver_logic():
    src_path = "/home/user/math-ws-proxy/src"
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    try:
        from math_ws.solver import solve_diophantine
    except ImportError as e:
        pytest.fail(f"Could not import solve_diophantine: {e}")

    # Test cases: a*x + b*y = c
    # 3x + 4y = 25 -> smallest x=3, y=4 (3*3 + 4*4 = 9 + 16 = 25)
    assert solve_diophantine(3, 4, 25) == (3, 4), "Failed for 3x + 4y = 25"

    # 5x + 2y = 12 -> smallest x=2, y=1 (5*2 + 2*1 = 10 + 2 = 12)
    assert solve_diophantine(5, 2, 12) == (2, 1), "Failed for 5x + 2y = 12"

    # 2x + 4y = 5 -> no integer solution
    assert solve_diophantine(2, 4, 5) is None, "Failed for 2x + 4y = 5, should be None"

    # 10x + 15y = 100 -> x=1, y=6 (10 + 90 = 100) or x=4, y=4 or x=7, y=2
    # Smallest positive x is 1
    assert solve_diophantine(10, 15, 100) == (1, 6), "Failed for 10x + 15y = 100, should return smallest positive x"

def test_v2_db_migration():
    db_path = "/home/user/math-ws-proxy/v2.db"
    assert os.path.isfile(db_path), f"Database {db_path} was not created"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, a, b, c FROM parsed_requests ORDER BY id ASC;")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query parsed_requests table: {e}")
    finally:
        conn.close()

    expected_rows = [
        (1, 3, 4, 25),
        (2, 5, 2, 12),
        (3, 10, 15, 100)
    ]
    assert rows == expected_rows, f"Data in v2.db does not match expected parsed values. Got {rows}"

def test_nginx_conf():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx configuration {conf_path} does not exist"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "Upgrade $http_upgrade" in content, "Missing 'Upgrade $http_upgrade' in nginx.conf"
    assert "Connection" in content and "upgrade" in content.lower(), "Missing 'Connection \"upgrade\"' in nginx.conf"
    assert "proxy_pass http://127.0.0.1:9000" in content or "proxy_pass http://localhost:9000" in content, "Missing proxy_pass to port 9000"

    # Test nginx configuration syntax
    result = subprocess.run(["nginx", "-t", "-c", conf_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Nginx configuration test failed:\n{result.stderr}"