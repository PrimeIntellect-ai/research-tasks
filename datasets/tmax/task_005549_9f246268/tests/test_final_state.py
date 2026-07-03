# test_final_state.py
import json
import os
import pytest

def test_final_billing_json_exists():
    assert os.path.isfile('/home/user/final_billing.json'), "The /home/user/final_billing.json file is missing."

def test_final_billing_json_content():
    with open('/home/user/final_billing.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The /home/user/final_billing.json file does not contain valid JSON.")

    assert "total_revenue" in data, "Missing 'total_revenue' in JSON."
    assert "users" in data, "Missing 'users' in JSON."

    assert data["total_revenue"] == 13.5, f"Expected total_revenue to be 13.5, got {data['total_revenue']}."

    users = data["users"]
    assert "user1" in users, "Missing 'user1' in users dictionary."
    assert "user2" in users, "Missing 'user2' in users dictionary."

    assert users["user1"] == 9.5, f"Expected user1 cost to be 9.5, got {users['user1']}."
    assert users["user2"] == 4.0, f"Expected user2 cost to be 4.0, got {users['user2']}."

def test_billing_processor_fixes():
    assert os.path.isfile('/home/user/billing_processor.py'), "The billing_processor.py script is missing."
    with open('/home/user/billing_processor.py', 'r') as f:
        content = f.read()

    # Check for sorting
    assert "sort" in content or "sorted(" in content, "The script does not appear to sort the events chronologically."

    # Check for thread safety fix (unsafe concatenation removed)
    assert "all_events = all_events + local_events" not in content, "The unsafe list concatenation is still present in billing_processor.py."