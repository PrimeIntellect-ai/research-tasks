# test_final_state.py

import os
import json
import pytest

def test_audit_script_exists():
    """Test that the audit.py script was created."""
    script_path = "/home/user/audit.py"
    assert os.path.exists(script_path), f"Audit script is missing at {script_path}"
    assert os.path.isfile(script_path), f"Audit script {script_path} is not a file"

def test_flagged_accounts_output():
    """Test that the flagged_accounts.json output file exists and is correctly formatted."""
    output_path = "/home/user/flagged_accounts.json"
    assert os.path.exists(output_path), f"Output file is missing at {output_path}"

    with open(output_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_path} is not valid JSON")

    assert isinstance(results, list), "Output must be a JSON array"
    assert len(results) == 3, f"Expected exactly 3 accounts in the output, got {len(results)}"

    for item in results:
        assert isinstance(item, dict), "Each item in the output array must be a JSON object"
        assert "account" in item, "Each object must have an 'account' key"
        assert "pagerank" in item, "Each object must have a 'pagerank' key"
        assert isinstance(item["account"], str), "'account' must be a string"
        assert isinstance(item["pagerank"], (int, float)), "'pagerank' must be a number"

def test_flagged_accounts_correctness():
    """Test the correctness of the flagged accounts."""
    output_path = "/home/user/flagged_accounts.json"
    if not os.path.exists(output_path):
        pytest.skip("Output file missing, skipping correctness check")

    with open(output_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Output file invalid JSON, skipping correctness check")

    if len(results) != 3:
        pytest.skip("Output file does not contain 3 items, skipping correctness check")

    # Check sorting
    pageranks = [item["pagerank"] for item in results]
    assert pageranks == sorted(pageranks, reverse=True), "Output is not sorted in descending order by PageRank"

    # Check specific accounts
    assert results[0]["account"] == "AccC", "The highest PageRank account in a cycle should be AccC"

    valid_cycle_accounts = {"AccA", "AccB", "AccC", "AccD", "AccE"}
    for item in results:
        assert item["account"] in valid_cycle_accounts, f"Account {item['account']} is not part of a valid cycle"