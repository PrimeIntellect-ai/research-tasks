# test_final_state.py
import os

def test_team_output_txt():
    output_path = "/home/user/team_output.txt"
    assert os.path.isfile(output_path), f"File {output_path} does not exist. Did you run the compiled C++ program?"

    expected_lines = [
        "2,Bob,VP",
        "3,Charlie,VP",
        "4,Dave,Manager",
        "5,Eve,Manager",
        "6,Frank,Engineer"
    ]

    with open(output_path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == expected_lines, f"Content of {output_path} does not match expected output. Expected: {expected_lines}, but got: {content}"

def test_query_plan_txt():
    plan_path = "/home/user/query_plan.txt"
    assert os.path.isfile(plan_path), f"File {plan_path} does not exist. Did you save the EXPLAIN QUERY PLAN output?"

    with open(plan_path, "r") as f:
        content = f.read().upper()

    # Check for keywords indicating an EXPLAIN QUERY PLAN output for the nodes table
    has_scan_or_search = "SCAN" in content or "SEARCH" in content
    has_nodes = "NODES" in content

    assert has_scan_or_search, f"{plan_path} does not seem to contain a valid EXPLAIN QUERY PLAN output (missing SCAN or SEARCH)."
    assert has_nodes, f"{plan_path} does not seem to contain a valid EXPLAIN QUERY PLAN output (missing reference to 'nodes' table)."