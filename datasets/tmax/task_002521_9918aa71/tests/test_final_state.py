# test_final_state.py
import os
import json
import csv
import math

def test_generate_data_script_exists():
    assert os.path.isfile("/home/user/generate_data.py"), "generate_data.py is missing"

def test_validation_log():
    log_path = "/home/user/validation.log"
    assert os.path.isfile(log_path), "validation.log is missing"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "SUCCESS", f"Expected 'SUCCESS' in validation.log, got '{content}'"

def test_experiment_config():
    config_path = "/home/user/experiment_config.json"
    assert os.path.isfile(config_path), "experiment_config.json is missing"
    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            assert False, "experiment_config.json is not a valid JSON file"

    assert config.get("seed") == 42, f"Expected seed to be 42, got {config.get('seed')}"
    assert config.get("num_samples") == 1000, f"Expected num_samples to be 1000, got {config.get('num_samples')}"
    assert config.get("noise_mean") == 0.0, f"Expected noise_mean to be 0.0, got {config.get('noise_mean')}"
    assert config.get("noise_std") == 0.5, f"Expected noise_std to be 0.5, got {config.get('noise_std')}"

def test_training_data_csv():
    csv_path = "/home/user/training_data.csv"
    assert os.path.isfile(csv_path), "training_data.csv is missing"

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            assert False, "training_data.csv is empty"

        assert headers == ["x", "y"], f"CSV headers must be ['x', 'y'], got {headers}"

        rows = list(reader)
        assert len(rows) == 1000, f"CSV must have exactly 1000 data rows, found {len(rows)}"

        x_vals = []
        y_vals = []
        for i, row in enumerate(rows):
            assert len(row) == 2, f"Row {i+1} does not have exactly 2 columns"
            try:
                x_vals.append(float(row[0]))
                y_vals.append(float(row[1]))
            except ValueError:
                assert False, f"Row {i+1} contains non-numeric data: {row}"

    # Check x values (linspace 0 to 10*pi)
    assert abs(x_vals[0] - 0.0) < 1e-5, f"First x value should be 0.0, got {x_vals[0]}"
    assert abs(x_vals[-1] - 10 * math.pi) < 1e-5, f"Last x value should be 10*pi, got {x_vals[-1]}"

    # Check first y value to ensure seed was likely set correctly
    expected_first_y = 0.24835707650561636
    assert abs(y_vals[0] - expected_first_y) < 1e-2, f"First y value expected ~{expected_first_y}, got {y_vals[0]}"

    # Check empirical mean and variance of y
    mean_y = sum(y_vals) / len(y_vals)
    var_y_pop = sum((y - mean_y)**2 for y in y_vals) / len(y_vals)
    var_y_sample = sum((y - mean_y)**2 for y in y_vals) / (len(y_vals) - 1)

    assert -0.2 < mean_y < 0.2, f"Mean of y ({mean_y}) is not strictly between -0.2 and 0.2"
    assert (2.5 < var_y_pop < 4.0) or (2.5 < var_y_sample < 4.0), f"Variance of y ({var_y_pop}) is not strictly between 2.5 and 4.0"