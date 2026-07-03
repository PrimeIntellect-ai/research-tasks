# test_final_state.py

import json
import os
import pytest

REPORT_PATH = '/home/user/test_report.json'
POSTERIORS_PATH = '/home/user/output/posteriors.json'

def test_report_exists():
    assert os.path.exists(REPORT_PATH), f"{REPORT_PATH} was not created."
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file."

def test_report_structure_and_types():
    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} is not valid JSON.")

    expected_keys = {
        "is_reproducible",
        "is_symmetric",
        "top_3_similar_to_0",
        "highest_ctr_item",
        "highest_ctr_value"
    }

    missing_keys = expected_keys - set(report.keys())
    assert not missing_keys, f"Missing keys in test_report.json: {missing_keys}"

    assert isinstance(report["is_reproducible"], bool), "'is_reproducible' must be a boolean."
    assert isinstance(report["is_symmetric"], bool), "'is_symmetric' must be a boolean."

    assert isinstance(report["top_3_similar_to_0"], list), "'top_3_similar_to_0' must be a list."
    assert len(report["top_3_similar_to_0"]) == 3, "'top_3_similar_to_0' must contain exactly 3 items."
    assert all(isinstance(x, int) for x in report["top_3_similar_to_0"]), "All items in 'top_3_similar_to_0' must be integers."
    assert 0 not in report["top_3_similar_to_0"], "Item 0 should be excluded from its own top 3 similar items."

    assert isinstance(report["highest_ctr_item"], int), "'highest_ctr_item' must be an integer."
    assert isinstance(report["highest_ctr_value"], (int, float)), "'highest_ctr_value' must be a float."

def test_report_correctness():
    with open(REPORT_PATH, 'r') as f:
        report = json.load(f)

    assert report["is_reproducible"] is True, "The ETL pipeline should be reproducible with a fixed seed."
    assert report["is_symmetric"] is True, "The similarity matrix should be perfectly symmetric."

    # Derive expected highest CTR item and value from the generated posteriors.json
    assert os.path.exists(POSTERIORS_PATH), f"{POSTERIORS_PATH} is missing. The ETL script must be run to generate it."

    with open(POSTERIORS_PATH, 'r') as f:
        posteriors = json.load(f)

    max_ctr = -1.0
    max_item = -1

    for item_id_str, params in posteriors.items():
        alpha = params["alpha"]
        beta = params["beta"]
        ctr = alpha / (alpha + beta)

        if ctr > max_ctr:
            max_ctr = ctr
            max_item = int(item_id_str)

    expected_ctr_value = round(max_ctr, 4)

    assert report["highest_ctr_item"] == max_item, (
        f"Incorrect 'highest_ctr_item'. Expected {max_item}, got {report['highest_ctr_item']}."
    )

    assert abs(report["highest_ctr_value"] - expected_ctr_value) < 1e-4, (
        f"Incorrect 'highest_ctr_value'. Expected {expected_ctr_value}, got {report['highest_ctr_value']}."
    )