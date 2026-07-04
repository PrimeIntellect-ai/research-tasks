# test_final_state.py
import os
import json
import pytest

def test_customers_export_jsonl():
    export_path = "/home/user/customers_export.jsonl"
    assert os.path.isfile(export_path), f"Missing output file: {export_path}"

    reference_scores = {
        1: 221.075,
        2: 307.25,
        3: 41.0
    }

    actual_scores = {}
    with open(export_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON on line {line_num}: {line}")

            assert "_id" in data, f"Missing '_id' in JSON object on line {line_num}"
            assert "customer_value_score" in data, f"Missing 'customer_value_score' in JSON object on line {line_num}"

            customer_id = data["_id"]
            score = data["customer_value_score"]
            actual_scores[customer_id] = score

    assert len(actual_scores) == len(reference_scores), f"Expected {len(reference_scores)} customers, but found {len(actual_scores)}"

    mse = 0.0
    for cid, ref_score in reference_scores.items():
        assert cid in actual_scores, f"Missing customer_id {cid} in output"
        actual_score = actual_scores[cid]
        mse += (actual_score - ref_score) ** 2

    mse /= len(reference_scores)

    threshold = 0.1
    assert mse <= threshold, f"MSE of customer_value_score is {mse}, which is greater than the threshold {threshold}"