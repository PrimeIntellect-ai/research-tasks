# test_final_state.py
import urllib.request
import urllib.error
import json
import random
import subprocess
import socket
import pytest

def check_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        try:
            s.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False

def get_db_data():
    try:
        users_out = subprocess.check_output(
            ["psql", "-h", "127.0.0.1", "-U", "postgres", "-d", "rbac_db", "-t", "-c", "SELECT username FROM users LIMIT 100;"],
            env={"PGPASSWORD": "password"}
        ).decode("utf-8")
        users = [u.strip() for u in users_out.split('\n') if u.strip()]

        res_out = subprocess.check_output(
            ["psql", "-h", "127.0.0.1", "-U", "postgres", "-d", "rbac_db", "-t", "-c", "SELECT resource_name FROM permissions LIMIT 100;"],
            env={"PGPASSWORD": "password"}
        ).decode("utf-8")
        resources = [r.strip() for r in res_out.split('\n') if r.strip()]
        return users, resources
    except Exception:
        # Fallback if psql fails for some reason
        return [f"user_{i}" for i in range(100)], [f"resource_{i}" for i in range(100)]

def test_agent_api_running():
    assert check_port_open("127.0.0.1", 8080), "Agent API is not running on port 8080."

def test_fuzz_equivalence():
    assert check_port_open("127.0.0.1", 8081), "Oracle API is not running on port 8081."

    users, resources = get_db_data()
    users.extend(["nonexistent_user", "admin_user"])
    resources.extend(["nonexistent_resource", "top_secret_file"])

    random.seed(42)

    N = 50
    for i in range(N):
        u = random.choice(users)
        r = random.choice(resources)

        url_agent = f"http://127.0.0.1:8080/audit?username={u}&resource={r}"
        url_oracle = f"http://127.0.0.1:8081/audit?username={u}&resource={r}"

        try:
            req_agent = urllib.request.urlopen(url_agent, timeout=5)
            agent_data = json.loads(req_agent.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            pytest.fail(f"Agent API returned HTTP error {e.code} for {url_agent}")
        except Exception as e:
            pytest.fail(f"Failed to fetch from Agent API for {url_agent}: {e}")

        try:
            req_oracle = urllib.request.urlopen(url_oracle, timeout=5)
            oracle_data = json.loads(req_oracle.read().decode("utf-8"))
        except Exception as e:
            pytest.fail(f"Failed to fetch from Oracle API for {url_oracle}: {e}")

        # Compare
        assert agent_data.get("username") == oracle_data.get("username"), f"Mismatch in 'username' for input ({u}, {r})"
        assert agent_data.get("resource_name") == oracle_data.get("resource_name"), f"Mismatch in 'resource_name' for input ({u}, {r})"
        assert agent_data.get("authorized") == oracle_data.get("authorized"), f"Mismatch in 'authorized' for input ({u}, {r}). Agent: {agent_data}, Oracle: {oracle_data}"

        # Lists
        agent_roles = agent_data.get("granted_by_roles", [])
        oracle_roles = oracle_data.get("granted_by_roles", [])
        assert agent_roles == oracle_roles, f"Mismatch in 'granted_by_roles' for input ({u}, {r}). Agent: {agent_roles}, Oracle: {oracle_roles}"

        agent_ts = agent_data.get("recent_access_timestamps", [])
        oracle_ts = oracle_data.get("recent_access_timestamps", [])
        assert agent_ts == oracle_ts, f"Mismatch in 'recent_access_timestamps' for input ({u}, {r}). Agent: {agent_ts}, Oracle: {oracle_ts}"