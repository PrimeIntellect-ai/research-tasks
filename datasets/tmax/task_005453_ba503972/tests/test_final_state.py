# test_final_state.py
import os
import json
import pytest

def test_documents_json():
    filepath = '/home/user/output/documents.json'
    assert os.path.isfile(filepath), f"{filepath} does not exist. Did the script run and create it?"

    with open(filepath, 'r') as f:
        try:
            docs = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{filepath} is not valid JSON.")

    assert isinstance(docs, list), f"Expected {filepath} to contain a JSON array."
    assert len(docs) == 3, f"Expected 3 users in {filepath}, found {len(docs)}."

    # Check Alice
    alice = next((d for d in docs if d.get('user_id') == '1'), None)
    assert alice is not None, "User '1' (Alice) not found in documents.json."
    assert alice.get('name') == 'Alice', "User '1' name should be 'Alice'."

    orders = alice.get('orders', [])
    assert isinstance(orders, list), "Alice's 'orders' should be a list."
    assert len(orders) == 2, f"Expected 2 orders for Alice, found {len(orders)}."

    order_101 = next((o for o in orders if o.get('order_id') == '101'), None)
    assert order_101 is not None, "Order '101' not found for Alice."
    assert order_101.get('status') == 'completed', "Order '101' status should be 'completed'."

    items = order_101.get('items', [])
    assert isinstance(items, list), "Order '101' 'items' should be a list."
    assert len(items) == 2, f"Expected 2 items in order '101', found {len(items)}."

    item_501 = next((i for i in items if i.get('item_id') == '501'), None)
    assert item_501 is not None, "Item '501' not found in order '101'."
    assert item_501.get('product_name') == 'Widget A', "Item '501' product_name should be 'Widget A'."
    assert isinstance(item_501.get('price'), float), "Price should be a float."
    assert item_501['price'] == 25.50, "Price for item '501' should be 25.50."

def test_pipeline_json():
    filepath = '/home/user/output/pipeline.json'
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, 'r') as f:
        try:
            pipeline = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{filepath} is not valid JSON.")

    assert isinstance(pipeline, list), f"Expected {filepath} to contain a JSON array."
    assert len(pipeline) > 0, "Pipeline array is empty."

    pipeline_str = json.dumps(pipeline)
    assert '$unwind' in pipeline_str, "Pipeline must contain at least one $unwind stage."
    assert '$match' in pipeline_str, "Pipeline must contain at least one $match stage."
    assert '$group' in pipeline_str, "Pipeline must contain a $group stage."
    assert '$sort' in pipeline_str, "Pipeline must contain a $sort stage."
    assert '$limit' in pipeline_str, "Pipeline must contain a $limit stage."
    assert 'Widget' in pipeline_str, "Pipeline must filter by 'Widget'."
    assert 'completed' in pipeline_str, "Pipeline must filter by 'completed' status."

def test_indexes_json():
    filepath = '/home/user/output/indexes.json'
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, 'r') as f:
        try:
            indexes = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{filepath} is not valid JSON.")

    assert isinstance(indexes, list), f"Expected {filepath} to contain a JSON array."
    assert len(indexes) > 0, "Indexes array is empty."

    # Check that the first index contains keys
    first_index = indexes[0]
    assert isinstance(first_index, dict), "Index definition must be a JSON object."
    assert 'keys' in first_index, "Index definition must contain 'keys'."

    keys_str = json.dumps(first_index['keys'])
    assert 'orders.status' in keys_str or 'orders' in keys_str, "Optimal index should target 'orders.status' or 'orders'."