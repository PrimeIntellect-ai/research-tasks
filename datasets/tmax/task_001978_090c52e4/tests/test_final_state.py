# test_final_state.py

import os
import re

PROTOS_DIR = "/home/user/protos"
API_PROTO = os.path.join(PROTOS_DIR, "api.proto")
MODELS_PROTO = os.path.join(PROTOS_DIR, "models.proto")
AUTH_PROTO = os.path.join(PROTOS_DIR, "auth.proto")
BASE_PROTO = os.path.join(PROTOS_DIR, "base.proto")
TOPOSORT_SCRIPT = "/home/user/toposort.py"
BUILD_ORDER_LOG = "/home/user/build_order.log"

def test_base_proto_created_correctly():
    assert os.path.isfile(BASE_PROTO), f"File {BASE_PROTO} was not created."
    with open(BASE_PROTO, "r") as f:
        content = f.read()
    assert 'syntax = "proto3";' in content, f"{BASE_PROTO} is missing syntax declaration."
    assert 'message ApiResponse' in content, f"{BASE_PROTO} is missing 'message ApiResponse'."

def test_api_proto_refactored():
    assert os.path.isfile(API_PROTO), f"File {API_PROTO} does not exist."
    with open(API_PROTO, "r") as f:
        content = f.read()
    assert 'message ApiResponse' not in content, f"'message ApiResponse' was not removed from {API_PROTO}."
    assert re.search(r'import\s+"base\.proto"\s*;', content), f"{API_PROTO} does not import 'base.proto'."

def test_models_proto_refactored():
    assert os.path.isfile(MODELS_PROTO), f"File {MODELS_PROTO} does not exist."
    with open(MODELS_PROTO, "r") as f:
        content = f.read()
    assert re.search(r'import\s+"api\.proto"\s*;', content) is None, f"{MODELS_PROTO} should no longer import 'api.proto'."
    assert re.search(r'import\s+"base\.proto"\s*;', content), f"{MODELS_PROTO} does not import 'base.proto'."

def test_toposort_script_exists():
    assert os.path.isfile(TOPOSORT_SCRIPT), f"Script {TOPOSORT_SCRIPT} does not exist."

def test_build_order_log():
    assert os.path.isfile(BUILD_ORDER_LOG), f"Log file {BUILD_ORDER_LOG} was not created."
    with open(BUILD_ORDER_LOG, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_order = [
        "base.proto",
        "models.proto",
        "auth.proto",
        "api.proto"
    ]

    assert lines == expected_order, f"Build order in {BUILD_ORDER_LOG} is incorrect. Expected {expected_order}, got {lines}."