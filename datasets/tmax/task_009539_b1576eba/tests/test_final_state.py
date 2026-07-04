# test_final_state.py
import os
import csv
import json
import pytest

def test_scripts_exist_and_executable():
    pipeline_script = "/home/user/pipeline.py"
    bash_script = "/home/user/run_pipeline.sh"

    assert os.path.exists(pipeline_script), f"Python script {pipeline_script} does not exist."
    assert os.path.isfile(pipeline_script), f"{pipeline_script} is not a file."

    assert os.path.exists(bash_script), f"Bash script {bash_script} does not exist."
    assert os.path.isfile(bash_script), f"{bash_script} is not a file."
    assert os.access(bash_script, os.X_OK), f"Bash script {bash_script} is not executable."

def test_cleaned_data_exists_and_correct():
    cleaned_data_path = "/home/user/data/clean/cleaned_data.csv"

    assert os.path.exists(cleaned_data_path), f"Cleaned data file {cleaned_data_path} does not exist."
    assert os.path.isfile(cleaned_data_path), f"{cleaned_data_path} is not a file."

    with open(cleaned_data_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 20, f"Expected 20 data rows in cleaned dataset, found {len(rows)}."

    for i, row in enumerate(rows):
        # sensor_id
        sensor_id = row.get("sensor_id", "")
        assert sensor_id.startswith("GH-"), f"Row {i}: sensor_id '{sensor_id}' does not start with 'GH-'."

        # temperature
        try:
            temp = float(row.get("temperature", ""))
            assert 10.0 <= temp <= 40.0, f"Row {i}: temperature {temp} is out of bounds [10.0, 40.0]."
        except ValueError:
            pytest.fail(f"Row {i}: temperature '{row.get('temperature')}' is not a valid float.")

        # humidity
        try:
            hum = float(row.get("humidity", ""))
            assert 20.0 <= hum <= 90.0, f"Row {i}: humidity {hum} is out of bounds [20.0, 90.0]."
        except ValueError:
            pytest.fail(f"Row {i}: humidity '{row.get('humidity')}' is not a valid float.")

        # soil_moisture
        try:
            soil = float(row.get("soil_moisture", ""))
            assert 0.0 <= soil <= 100.0, f"Row {i}: soil_moisture {soil} is out of bounds [0.0, 100.0]."
        except ValueError:
            pytest.fail(f"Row {i}: soil_moisture '{row.get('soil_moisture')}' is not a valid float.")

        # yield_class
        try:
            yc = int(row.get("yield_class", ""))
            assert yc in {0, 1, 2}, f"Row {i}: yield_class {yc} is not in {{0, 1, 2}}."
        except ValueError:
            pytest.fail(f"Row {i}: yield_class '{row.get('yield_class')}' is not a valid integer.")

def test_model_exists():
    model_path = "/home/user/model/rf_model.pkl"
    assert os.path.exists(model_path), f"Model file {model_path} does not exist."
    assert os.path.isfile(model_path), f"{model_path} is not a file."
    assert os.path.getsize(model_path) > 0, f"Model file {model_path} is empty."

def test_metrics_exist_and_correct():
    metrics_path = "/home/user/report/metrics.json"

    assert os.path.exists(metrics_path), f"Metrics file {metrics_path} does not exist."
    assert os.path.isfile(metrics_path), f"{metrics_path} is not a file."

    with open(metrics_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Metrics file {metrics_path} does not contain valid JSON.")

    assert "accuracy" in metrics, "Key 'accuracy' is missing from metrics.json."
    assert isinstance(metrics["accuracy"], float), f"Value for 'accuracy' must be a float, found {type(metrics['accuracy']).__name__}."
    assert 0.0 <= metrics["accuracy"] <= 1.0, f"Accuracy {metrics['accuracy']} is out of bounds [0.0, 1.0]."