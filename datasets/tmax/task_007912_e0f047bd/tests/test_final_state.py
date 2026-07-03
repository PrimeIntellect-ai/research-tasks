# test_final_state.py
import os
import json

def test_required_files_exist():
    expected_files = [
        "/home/user/pipeline.py",
        "/home/user/test_pipeline.py",
        "/home/user/results.json",
        "/home/user/test_report.log"
    ]
    for filepath in expected_files:
        assert os.path.exists(filepath), f"Required file is missing: {filepath}"

def test_virtual_environment_exists():
    venv_python = "/home/user/venv/bin/python"
    venv_pytest = "/home/user/venv/bin/pytest"
    assert os.path.exists(venv_python), f"Virtual environment Python not found at {venv_python}"
    assert os.path.exists(venv_pytest), f"Virtual environment pytest not found at {venv_pytest}"

def test_results_json_content():
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"{results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{results_path} does not contain valid JSON."

    expected_keys = {"best_alpha", "cv_mae", "median_fan_speed"}
    assert set(results.keys()) == expected_keys, f"JSON keys must exactly match {expected_keys}, found {list(results.keys())}"

    assert isinstance(results["best_alpha"], (int, float)), "best_alpha must be a number."
    assert isinstance(results["cv_mae"], (int, float)), "cv_mae must be a number."
    assert isinstance(results["median_fan_speed"], (int, float)), "median_fan_speed must be a number."

    # Validate median fan speed (should be approx 3057.90)
    assert abs(results["median_fan_speed"] - 3057.90) <= 1.5, \
        f"median_fan_speed {results['median_fan_speed']} is not within the expected range."

    # Validate cv_mae
    assert 0.0 < results["cv_mae"] < 15.0, \
        f"cv_mae {results['cv_mae']} is not within the expected range (0.0 to 15.0)."

def test_pytest_report_success():
    report_path = "/home/user/test_report.log"
    assert os.path.exists(report_path), f"{report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().lower()

    assert "passed" in content, "The test_report.log does not indicate that the tests passed."

    # Check if the required tests are mentioned or if the file looks like a pytest output
    assert "test_pipeline.py" in content or "test session starts" in content, \
        "The test_report.log does not appear to be a valid pytest output."