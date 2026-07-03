# test_final_state.py

import os
import json
import pytest

def test_fixed_network_f1_score():
    output_path = "/home/user/fixed_network.json"
    assert os.path.isfile(output_path), f"Output file is missing at {output_path}"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {output_path} is not valid JSON")

    affected = {"User02", "User05", "User11", "User14"}
    pred_affected = set()

    for user, config in data.items():
        if isinstance(config, dict) and config.get("subnet") == "10.1.0.0/24":
            pred_affected.add(user)

    tp = len(affected & pred_affected)
    fp = len(pred_affected - affected)
    fn = len(affected - pred_affected)

    if (2 * tp + fp + fn) > 0:
        f1 = 2 * tp / (2 * tp + fp + fn)
    else:
        f1 = 0.0

    assert f1 >= 0.9, f"F1 score of correctly modified subnets is {f1:.3f}, expected >= 0.9. True affected: {affected}, Predicted affected: {pred_affected}"