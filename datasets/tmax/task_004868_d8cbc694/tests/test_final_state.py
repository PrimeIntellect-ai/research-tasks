# test_final_state.py

import os
import json
import time
import subprocess
import pytest

def test_executable_exists():
    executable = "/home/user/join_to_json"
    assert os.path.exists(executable), f"Executable {executable} does not exist. Did you compile the C++ program?"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_execution_time_and_output():
    executable = "/home/user/join_to_json"
    output_file = "/home/user/result.json"

    # Remove output if it exists from a previous run to ensure we measure fresh output
    if os.path.exists(output_file):
        os.remove(output_file)

    start_time = time.time()
    try:
        result = subprocess.run([executable], capture_output=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail("Execution timed out after 10 seconds. The program is far too slow.")
    end_time = time.time()

    assert result.returncode == 0, f"Executable failed with return code {result.returncode}. Stderr: {result.stderr.decode('utf-8', errors='replace')}"

    execution_time = end_time - start_time
    assert execution_time <= 1.5, f"Execution time {execution_time:.3f}s exceeded threshold of 1.5s. Your indexing strategy might be inefficient."

    assert os.path.exists(output_file), f"Output JSON file {output_file} was not created."

    with open(output_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output in {output_file} is not valid JSON: {e}")

    assert isinstance(data, list), "Root of the output JSON must be an array."

    # Basic structural validation
    if len(data) > 0:
        first_user = data[0]
        assert "user_id" in first_user, "User object is missing 'user_id' key."
        assert "orders" in first_user, "User object is missing 'orders' key."
        assert isinstance(first_user["orders"], list), "'orders' value must be an array."

        # Check that empty orders are skipped (requirement 4)
        for user in data:
            assert len(user.get("orders", [])) > 0, f"User {user.get('user_id')} has no orders, but should have been skipped."
            for order in user["orders"]:
                assert len(order.get("items", [])) > 0, f"Order {order.get('order_id')} has no items, but should have been skipped."

        if len(first_user["orders"]) > 0:
            first_order = first_user["orders"][0]
            assert "order_id" in first_order, "Order object is missing 'order_id' key."
            assert "items" in first_order, "Order object is missing 'items' key."
            assert isinstance(first_order["items"], list), "'items' value must be an array."

            if len(first_order["items"]) > 0:
                first_item = first_order["items"][0]
                assert "item_id" in first_item, "Item object is missing 'item_id' key."