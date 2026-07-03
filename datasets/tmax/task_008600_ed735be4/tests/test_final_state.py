# test_final_state.py
import os
import json
import math

def test_final_report_exists_and_correct():
    file_path = "/home/user/final_report.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you export the results?"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} is not valid JSON."

    assert isinstance(data, list), "The JSON output should be an array of objects."
    assert len(data) == 3, f"Expected exactly 3 records in the final report after pagination, got {len(data)}."

    expected = [
        {"_id": "F", "average_cost": 30.0, "successful_orders": 1},
        {"_id": "C", "average_cost": 24.0, "successful_orders": 2},
        {"_id": "B", "average_cost": 20.0, "successful_orders": 1}
    ]

    for i in range(3):
        actual_id = data[i].get("_id")
        expected_id = expected[i]["_id"]
        assert actual_id == expected_id, f"Record {i} expected _id '{expected_id}', got '{actual_id}'"

        actual_cost = data[i].get("average_cost")
        expected_cost = expected[i]["average_cost"]
        assert actual_cost is not None, f"Record {i} missing 'average_cost'"
        assert math.isclose(actual_cost, expected_cost, rel_tol=1e-5), \
            f"Record {i} expected average_cost {expected_cost}, got {actual_cost}"

        actual_orders = data[i].get("successful_orders")
        expected_orders = expected[i]["successful_orders"]
        assert actual_orders == expected_orders, \
            f"Record {i} expected successful_orders {expected_orders}, got {actual_orders}"