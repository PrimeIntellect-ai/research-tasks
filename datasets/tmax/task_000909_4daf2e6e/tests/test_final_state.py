# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/generate_routes.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_routes_conf_content():
    conf_path = "/home/user/routes.conf"
    assert os.path.isfile(conf_path), f"Configuration file {conf_path} does not exist."

    expected_lines = [
        "ProxyPass /core http://localhost:8080/core",
        "ProxyPass /auth http://localhost:8080/auth",
        "ProxyPass /billing http://localhost:8080/billing",
        "ProxyPass /api http://localhost:8080/api",
        "ProxyPass /frontend http://localhost:8080/frontend"
    ]

    with open(conf_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {conf_path} do not match the expected topological sort output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )