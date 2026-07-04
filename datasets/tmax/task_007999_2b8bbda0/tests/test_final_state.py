# test_final_state.py

import os
import json
import ast

def test_server_fixed_exists():
    fixed_script = "/home/user/app/server_fixed.py"
    assert os.path.isfile(fixed_script), f"Fixed server script {fixed_script} does not exist."

def test_server_fixed_uses_parameterized_queries():
    fixed_script = "/home/user/app/server_fixed.py"
    assert os.path.isfile(fixed_script), f"Fixed server script {fixed_script} does not exist."

    with open(fixed_script, 'r') as f:
        source = f.read()

    tree = ast.parse(source)

    # Find all calls to cursor.execute
    execute_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'execute':
                execute_calls.append(node)

    assert len(execute_calls) > 0, "No cursor.execute calls found in the fixed script."

    # Ensure that at least one execute call (the one querying users) uses parameterized queries
    # i.e., it has more than 1 argument, or the first argument is not an f-string/JoinedStr/BinOp
    safe_query_found = False
    for call in execute_calls:
        if not call.args:
            continue
        first_arg = call.args[0]

        # If it's a string literal, we check if it's the SELECT query
        is_select = False
        if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
            if 'SELECT' in first_arg.value.upper() and 'FROM USERS' in first_arg.value.upper():
                is_select = True

        if is_select:
            # It must have a second argument for parameters
            assert len(call.args) > 1, "The SELECT query in cursor.execute does not use parameterized arguments."
            safe_query_found = True

    # If we couldn't definitively identify the SELECT query by string literal, 
    # let's just make sure no f-strings or format/concat are used in execute calls that look like the target
    if not safe_query_found:
        for call in execute_calls:
            first_arg = call.args[0]
            if isinstance(first_arg, ast.JoinedStr):
                # If it's an f-string, check if it's the SELECT query
                for value in first_arg.values:
                    if isinstance(value, ast.Constant) and isinstance(value.value, str):
                        if 'SELECT' in value.value.upper():
                            assert False, "Found an f-string used for a SELECT query in cursor.execute. Use parameterized queries."
            elif isinstance(first_arg, ast.BinOp):
                assert False, "Found string concatenation/formatting used in cursor.execute. Use parameterized queries."

def test_policy_json_exists_and_correct():
    policy_file = "/home/user/policy.json"
    assert os.path.isfile(policy_file), f"Policy file {policy_file} does not exist."

    with open(policy_file, 'r') as f:
        try:
            policy_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Policy file {policy_file} is not valid JSON."

    assert "blocked_entities" in policy_data, "Policy JSON is missing the 'blocked_entities' key."

    blocked = policy_data["blocked_entities"]
    assert isinstance(blocked, list), "'blocked_entities' must be a list."

    expected_blocked = [
        {
            "ip": "192.168.1.105",
            "client_id": "malicious_client_99"
        }
    ]

    assert len(blocked) == len(expected_blocked), f"Expected {len(expected_blocked)} blocked entities, found {len(blocked)}."

    # Sort both to ensure order doesn't fail the test if there was more than 1, though task says sort by ip
    blocked_sorted = sorted(blocked, key=lambda x: x.get("ip", ""))
    expected_sorted = sorted(expected_blocked, key=lambda x: x["ip"])

    assert blocked_sorted == expected_sorted, f"Blocked entities do not match expected output. Got {blocked_sorted}, expected {expected_sorted}."