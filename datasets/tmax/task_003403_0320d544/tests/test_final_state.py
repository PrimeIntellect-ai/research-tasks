# test_final_state.py

import os
import pytest

def test_router_c_exists():
    assert os.path.isfile("/home/user/router.c"), "/home/user/router.c does not exist."

def test_router_executable_exists():
    assert os.path.isfile("/home/user/router"), "/home/user/router executable does not exist."
    assert os.access("/home/user/router", os.X_OK), "/home/user/router is not executable."

def test_router_c_contains_required_sql_features():
    with open("/home/user/router.c", "r") as f:
        content = f.read().upper()

    assert "WITH RECURSIVE" in content, "The C code does not seem to use a 'WITH RECURSIVE' CTE."
    assert "OVER" in content and ("PARTITION BY" in content or "ROW_NUMBER" in content or "MAX" in content), \
        "The C code does not seem to use window functions to filter stale records."
    assert "CORE_1" in content, "The C code does not contain the starting node 'CORE_1'."
    assert "EDGE_7" in content, "The C code does not contain the ending node 'EDGE_7'."

def test_optimal_route_output():
    output_file = "/home/user/optimal_route.txt"
    assert os.path.isfile(output_file), f"{output_file} does not exist. Did you run the compiled program?"

    with open(output_file, "r") as f:
        content = f.read().strip()

    expected_output = "CORE_1->DIST_2->EDGE_7,20"
    assert content == expected_output, f"Output file content is incorrect. Expected '{expected_output}', got '{content}'."