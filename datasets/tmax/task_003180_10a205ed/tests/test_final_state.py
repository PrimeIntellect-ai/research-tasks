# test_final_state.py

import os
import json
import pytest

def test_config_updated():
    config_path = "/home/user/microservices/config.json"
    assert os.path.isfile(config_path), f"File {config_path} does not exist."

    with open(config_path, 'r') as f:
        config = json.load(f)

    assert config.get("email_port") == 8025, f"Expected email_port to be 8025, but got {config.get('email_port')}."
    assert config.get("api_ports") == [8081, 8082], "api_ports should remain [8081, 8082]."
    assert config.get("proxy_port") == 8080, "proxy_port should remain 8080."

def test_router_script_exists():
    router_path = "/home/user/router.py"
    assert os.path.isfile(router_path), f"Router script {router_path} does not exist."

def test_verify_script_exists():
    verify_path = "/home/user/verify.sh"
    assert os.path.isfile(verify_path), f"Verification script {verify_path} does not exist."

def test_routing_log_contents():
    log_path = "/home/user/routing.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    expected_1 = "API_RESPONSE_8081API_RESPONSE_8082EMAIL_SERVICE_ACK"
    expected_2 = "API_RESPONSE_8082API_RESPONSE_8081EMAIL_SERVICE_ACK"

    assert content in (expected_1, expected_2), (
        f"routing.log content does not match the expected round-robin output.\n"
        f"Got: '{content}'\n"
        f"Expected either '{expected_1}' or '{expected_2}'."
    )