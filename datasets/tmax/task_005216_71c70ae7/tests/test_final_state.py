# test_final_state.py
import os
import json
import re

def get_manifest():
    manifest_path = "/home/user/manifest.json"
    with open(manifest_path, 'r') as f:
        return json.load(f)

def test_build_order_txt():
    build_order_path = "/home/user/build_order.txt"
    assert os.path.isfile(build_order_path), f"{build_order_path} does not exist."

    with open(build_order_path, 'r') as f:
        content = f.read().strip()

    order = [x.strip() for x in content.split(',') if x.strip()]

    expected_orders = [
        ["db-migration", "auth-service", "user-service", "api-gateway", "frontend"],
        ["db-migration", "user-service", "auth-service", "api-gateway", "frontend"]
    ]

    assert order in expected_orders, f"Invalid topological sort in build_order.txt: {order}"

def test_build_all_sh():
    build_all_path = "/home/user/build_all.sh"
    assert os.path.isfile(build_all_path), f"{build_all_path} does not exist."

    with open(build_all_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_commands = {
        "db-migration": "bash db-migration.sh",
        "auth-service": "cargo build --release --bin auth-service",
        "user-service": "cargo build --release --bin user-service",
        "api-gateway": "cargo build --release --bin api-gateway",
        "frontend": "npm install && npm run build --prefix frontend"
    }

    expected_file_1 = [
        expected_commands["db-migration"],
        expected_commands["auth-service"],
        expected_commands["user-service"],
        expected_commands["api-gateway"],
        expected_commands["frontend"]
    ]

    expected_file_2 = [
        expected_commands["db-migration"],
        expected_commands["user-service"],
        expected_commands["auth-service"],
        expected_commands["api-gateway"],
        expected_commands["frontend"]
    ]

    assert lines in [expected_file_1, expected_file_2], f"Invalid commands or order in build_all.sh: {lines}"

def test_nginx_conf():
    nginx_conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"{nginx_conf_path} does not exist."

    with open(nginx_conf_path, 'r') as f:
        content = f.read()

    # Check for basic structure
    assert "events" in content, "nginx.conf missing 'events' block."
    assert "http" in content, "nginx.conf missing 'http' block."
    assert "server" in content, "nginx.conf missing 'server' block."
    assert "listen 8080;" in content, "nginx.conf missing 'listen 8080;'."

    # Extract locations
    locations = re.findall(r'location\s+([^\s]+)\s*\{\s*proxy_pass\s+http://127\.0\.0\.1:(\d+);\s*\}', content)

    expected_locations = [
        ("/", "3000"),
        ("/api", "8082"),
        ("/auth", "8081"),
        ("/users", "8083")
    ]

    assert locations == expected_locations, f"Locations in nginx.conf are missing, incorrect, or not sorted alphabetically by route. Found: {locations}"