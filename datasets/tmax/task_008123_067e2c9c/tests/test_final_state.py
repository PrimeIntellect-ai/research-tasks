# test_final_state.py
import os
import json
import pytest

BASE_DIR = "/home/user/waf_test_env"
WAF_ANALYZER = os.path.join(BASE_DIR, "waf_analyzer")
RULES_GRAPH = os.path.join(BASE_DIR, "rules_graph.txt")
RESOLVE_RULES = os.path.join(BASE_DIR, "resolve_rules.py")
EXECUTION_PLAN = os.path.join(BASE_DIR, "execution_plan.json")

def test_waf_analyzer_built():
    """Test that the waf_analyzer binary was successfully built."""
    assert os.path.isfile(WAF_ANALYZER), f"Binary {WAF_ANALYZER} is missing. Did you run make?"
    assert os.access(WAF_ANALYZER, os.X_OK), f"File {WAF_ANALYZER} is not executable."

def test_rules_graph_generated():
    """Test that rules_graph.txt was generated."""
    assert os.path.isfile(RULES_GRAPH), f"File {RULES_GRAPH} is missing. Did you run the analyzer?"
    with open(RULES_GRAPH, "r") as f:
        content = f.read()
    assert "Rule:init_req" in content, "rules_graph.txt does not contain the expected rule output."

def test_resolve_rules_script_exists():
    """Test that the Python script resolve_rules.py exists."""
    assert os.path.isfile(RESOLVE_RULES), f"Python script {RESOLVE_RULES} is missing."

def test_execution_plan_json():
    """Test that execution_plan.json exists and contains the correct sorted array."""
    assert os.path.isfile(EXECUTION_PLAN), f"JSON file {EXECUTION_PLAN} is missing."

    with open(EXECUTION_PLAN, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{EXECUTION_PLAN} is not valid JSON.")

    expected_plan = [
        "init_req",
        "rate_limit",
        "parse_headers",
        "check_xss",
        "check_sqli",
        "forward_req"
    ]

    assert isinstance(data, list), "The JSON output must be a list of strings."
    assert data == expected_plan, f"Execution plan incorrect. Expected {expected_plan}, but got {data}."