# test_final_state.py

import os
import csv
import pytest

def test_libstatboot_compiled():
    """Check if the shared library was successfully compiled."""
    so_path = '/app/libstatboot-1.2/libstatboot.so'
    assert os.path.isfile(so_path), f"Shared library {so_path} does not exist. Did you fix the Makefile and compile?"

def test_etl_pipeline_source_exists():
    """Check if the ETL pipeline C source code exists."""
    c_path = '/home/user/etl_pipeline.c'
    assert os.path.isfile(c_path), f"Source file {c_path} does not exist."

def test_bootstrap_result_exists():
    """Check if the pipeline output file exists."""
    txt_path = '/home/user/bootstrap_result.txt'
    assert os.path.isfile(txt_path), f"Output file {txt_path} does not exist. Did you run your pipeline?"

def test_bootstrap_result_value():
    """Check if the computed bootstrap mean is within the acceptable threshold."""
    # Recompute the expected mean based on the actual CSV file
    csv_path = '/home/user/sensor_data.csv'
    assert os.path.isfile(csv_path), f"Data file {csv_path} is missing."

    valid_temps = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            temp_str = row.get('temperature', '').strip()
            if not temp_str:
                continue
            try:
                temp = float(temp_str)
                if -50.0 <= temp <= 100.0:
                    valid_temps.append(temp)
            except ValueError:
                continue

    assert len(valid_temps) > 0, "No valid temperatures found in the dataset to compute expected mean."
    expected_mean = sum(valid_temps) / len(valid_temps)

    # Read the agent's result
    txt_path = '/home/user/bootstrap_result.txt'
    with open(txt_path, 'r') as f:
        agent_val_str = f.read().strip()

    try:
        agent_val = float(agent_val_str)
    except ValueError:
        pytest.fail(f"Could not parse the result in {txt_path} as a float. Found: '{agent_val_str}'")

    # Compare the agent's value with the expected mean
    diff = abs(agent_val - expected_mean)
    threshold = 0.5

    assert diff <= threshold, (
        f"Computed bootstrap mean is inaccurate.\n"
        f"Agent value: {agent_val}\n"
        f"Reference mean: {expected_mean}\n"
        f"Absolute difference: {diff} (Threshold is <= {threshold})"
    )