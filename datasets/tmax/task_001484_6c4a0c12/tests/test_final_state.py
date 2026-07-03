# test_final_state.py
import json
import os
import pytest

def test_final_profile_accuracy():
    output_path = "/home/user/final_profile.json"
    assert os.path.exists(output_path), f"Output file missing at {output_path}"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON.")

    score = 0.0

    # Check customer_id
    if data.get("customer_id") == "CUST-8924":
        score += 0.25

    # Check average_resolution_time
    avg_res_time = data.get("average_resolution_time", 0)
    if isinstance(avg_res_time, (int, float)) and abs(avg_res_time - 18.25) < 0.1:
        score += 0.25

    # Check target_category_spend
    spend = data.get("target_category_spend", 0)
    if isinstance(spend, (int, float)) and abs(spend - 400.0) < 0.1:
        score += 0.25

    # Check unique_issues
    issues = data.get("unique_issues", [])
    if isinstance(issues, list) and set(issues) == {"Defect", "Billing"}:
        score += 0.25

    assert score >= 1.0, f"Accuracy score {score} is below the threshold of 1.0. Parsed data: {data}"