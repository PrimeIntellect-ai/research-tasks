# test_final_state.py

import os
import json
import math
import pytest

def test_benchmark_metrics_exists():
    assert os.path.isfile("/home/user/benchmark_metrics.json"), (
        "The file /home/user/benchmark_metrics.json was not found. "
        "Did you run 'cargo run --release' successfully?"
    )

def test_data_leakage_fixed():
    with open("/home/user/benchmark_metrics.json", "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/benchmark_metrics.json is not valid JSON.")

    assert "test_set_normalized" in metrics, (
        "The key 'test_set_normalized' is missing from benchmark_metrics.json"
    )

    normalized_test = metrics["test_set_normalized"]
    assert isinstance(normalized_test, list), "test_set_normalized should be a list"
    assert len(normalized_test) == 2, "test_set_normalized should contain exactly 2 elements"

    # Calculate expected values
    train_data = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0]
    test_data = [90.0, 100.0]

    mean = sum(train_data) / len(train_data)
    variance = sum((x - mean) ** 2 for x in train_data) / len(train_data)
    std_dev = math.sqrt(variance)

    expected_normalized = [(x - mean) / std_dev for x in test_data]

    for actual, expected in zip(normalized_test, expected_normalized):
        assert math.isclose(actual, expected, rel_tol=1e-5), (
            f"Data leakage bug not fixed correctly. Expected normalized value close to {expected}, "
            f"but got {actual}."
        )

def test_schema_enforcement_remains():
    main_rs_path = "/home/user/bayes_pipeline/src/main.rs"
    assert os.path.isfile(main_rs_path), "src/main.rs is missing"

    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "<= 0.0" in content, "Schema enforcement (checking for <= 0.0) appears to be removed."
    assert "panic!" in content, "Schema enforcement panic appears to be removed."