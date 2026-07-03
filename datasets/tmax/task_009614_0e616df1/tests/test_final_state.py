# test_final_state.py
import os
import json
import csv
from collections import defaultdict

def test_build_model_script_exists():
    script_path = "/home/user/build_model.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path} was not found."

def test_item_probs_json_exists():
    json_path = "/home/user/item_probs.json"
    assert os.path.isfile(json_path), f"Output file missing: {json_path} was not found."

def test_item_probs_logic_and_format():
    json_path = "/home/user/item_probs.json"
    csv_path = "/home/user/raw_logs.csv"

    assert os.path.isfile(csv_path), "Initial raw_logs.csv is missing."

    # Derive expected result from the CSV
    user_items = defaultdict(set)
    item_users = defaultdict(set)

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["action_type"] == "purchase":
                u = row["user_id"]
                i = row["item_id"]
                user_items[u].add(i)
                item_users[i].add(u)

    expected_probs = {}
    for x in item_users:
        x_users = item_users[x]
        x_count = len(x_users)

        y_counts = defaultdict(int)
        for u in x_users:
            for y in user_items[u]:
                if y != x:
                    y_counts[y] += 1

        probs = []
        for y, count in y_counts.items():
            prob = round(count / x_count, 2)
            probs.append({"item": y, "prob": prob})

        # Sort by prob descending, then item ascending
        probs.sort(key=lambda d: (-d["prob"], d["item"]))
        expected_probs[x] = probs

    # Read the generated JSON
    with open(json_path, "r") as f:
        try:
            actual_probs = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    # Check keys
    expected_keys = set(expected_probs.keys())
    actual_keys = set(actual_probs.keys())
    assert actual_keys == expected_keys, f"Expected items {expected_keys}, but got {actual_keys}."

    # Check values and sorting
    for x in expected_keys:
        expected_list = expected_probs[x]
        actual_list = actual_probs[x]

        assert len(actual_list) == len(expected_list), f"Item {x} has incorrect number of recommended items."

        for i, (exp, act) in enumerate(zip(expected_list, actual_list)):
            assert act["item"] == exp["item"], f"For item {x}, recommendation at index {i} should be {exp['item']}, got {act.get('item')}."

            # Allow float or string for prob, but check value
            act_prob = float(act["prob"])
            assert act_prob == exp["prob"], f"For item {x}, recommendation {exp['item']} should have prob {exp['prob']}, got {act_prob}."

            # If the student output string, ensure it has 2 decimal places if required,
            # but standard JSON parser reads them as floats. We just check the float value.
            # The prompt says "Probabilities must be rounded to exactly 2 decimal places (e.g., 0.75, 1.00)."
            # If they used strings, we can check format. If floats, 1.00 becomes 1.0.
            # We'll just enforce the mathematical value is correct to 2 decimal places.