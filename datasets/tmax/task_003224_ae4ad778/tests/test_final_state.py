# test_final_state.py
import os
import json

def test_artifacts_directory_exists():
    assert os.path.isdir("/home/user/artifacts"), "Artifacts directory does not exist at /home/user/artifacts"

def test_run_metrics_json_exists():
    assert os.path.isfile("/home/user/artifacts/run_metrics.json"), "run_metrics.json does not exist in /home/user/artifacts"

def test_run_metrics_json_content():
    json_path = "/home/user/artifacts/run_metrics.json"
    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not a valid JSON file"

    expected_keys = {"mean_accuracy", "ci_lower", "ci_upper"}
    actual_keys = set(data.keys())
    assert expected_keys.issubset(actual_keys), f"JSON file is missing keys. Expected {expected_keys}, got {actual_keys}"

    mean_accuracy = data["mean_accuracy"]
    ci_lower = data["ci_lower"]
    ci_upper = data["ci_upper"]

    assert isinstance(mean_accuracy, (int, float)), "mean_accuracy must be a number"
    assert isinstance(ci_lower, (int, float)), "ci_lower must be a number"
    assert isinstance(ci_upper, (int, float)), "ci_upper must be a number"

    assert abs(mean_accuracy - 0.82992) < 1e-4, f"mean_accuracy {mean_accuracy} is incorrect. Expected ~0.82992"
    assert abs(ci_lower - 0.82424) < 1e-4, f"ci_lower {ci_lower} is incorrect. Expected ~0.82424"
    assert abs(ci_upper - 0.83512) < 1e-4, f"ci_upper {ci_upper} is incorrect. Expected ~0.83512"