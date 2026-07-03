# test_final_state.py
import os
import sqlite3
import json
import urllib.request
import urllib.error

def test_database_contents():
    db_path = "/home/user/app.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username, role FROM users ORDER BY username;")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        assert False, f"Failed to query database: {e}"
    finally:
        conn.close()

    expected = [("alice", "admin"), ("bob", "dev"), ("charlie", "dev")]
    assert rows == expected, f"Database contents do not match expected. Got: {rows}"

def test_active_port_file():
    port_file = "/home/user/active_port.txt"
    assert os.path.exists(port_file), f"{port_file} does not exist."
    with open(port_file, "r") as f:
        port = f.read().strip()
    assert port == "8080", f"Expected active port to be 8080, got {port}."

def test_active_pid_file_and_process():
    pid_file = "/home/user/active_pid.txt"
    assert os.path.exists(pid_file), f"{pid_file} does not exist."
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} from active_pid.txt is not running."

    # Check if process is api.py
    cmdline_file = f"/proc/{pid}/cmdline"
    assert os.path.exists(cmdline_file), f"Process {pid} exists but cannot read cmdline."
    with open(cmdline_file, "r") as f:
        cmdline = f.read().replace('\0', ' ')
    assert "api.py" in cmdline, f"Process {pid} is not api.py. Cmdline: {cmdline}"

def test_api_responds_on_8080():
    url = "http://localhost:8080/users"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert isinstance(data, list), "Expected a JSON array."
            assert len(data) == 3, "Expected 3 users in the response."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to API on port 8080: {e}"

def test_deployment_test_json():
    json_path = "/home/user/deployment_test.json"
    assert os.path.exists(json_path), f"{json_path} does not exist."
    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} does not contain valid JSON."

    expected_users = [
        {"username": "alice", "role": "admin"},
        {"username": "bob", "role": "dev"},
        {"username": "charlie", "role": "dev"}
    ]

    # Sort both lists by username for comparison
    data_sorted = sorted(data, key=lambda x: x.get("username", ""))
    expected_sorted = sorted(expected_users, key=lambda x: x.get("username", ""))

    assert data_sorted == expected_sorted, f"JSON contents do not match expected. Got: {data_sorted}"

def test_only_one_api_instance():
    # Check process list for api.py
    api_pids = []
    for pid in os.listdir('/proc'):
        if pid.isdigit():
            try:
                with open(f"/proc/{pid}/cmdline", "r") as f:
                    cmdline = f.read().replace('\0', ' ')
                if "python" in cmdline and "api.py" in cmdline:
                    api_pids.append(pid)
            except IOError:
                continue

    assert len(api_pids) == 1, f"Expected exactly one instance of api.py running, found {len(api_pids)}: {api_pids}"