# test_final_state.py

import os
import json
import sys
import subprocess
import re
import pytest

def test_config_recovered():
    """Verify that config.json was recovered and is valid."""
    config_path = "/app/worker/config.json"
    assert os.path.exists(config_path), f"config.json was not recovered to {config_path}."

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{config_path} is not a valid JSON file.")

    assert "batch_size" in config, "Recovered config.json is missing 'batch_size' key."
    assert "redis_host" in config, "Recovered config.json is missing 'redis_host' key."
    assert "redis_port" in config, "Recovered config.json is missing 'redis_port' key."

def test_output_file_exists():
    """Verify that the worker produced the totals.csv file."""
    output_path = "/app/worker/output/totals.csv"
    assert os.path.exists(output_path), f"Output file {output_path} was not generated. The pipeline may have crashed or not run."
    assert os.path.getsize(output_path) > 0, f"Output file {output_path} is empty."

def test_mse_metric():
    """
    Verify that the MSE of the aggregated totals is within the acceptable threshold (<= 1e-10).
    Uses the provided evaluation script to compute the metric.
    """
    output_path = "/app/worker/output/totals.csv"
    eval_script = "/app/tests/evaluate_mse.py"

    assert os.path.exists(output_path), f"Missing {output_path}"
    assert os.path.exists(eval_script), f"Missing evaluation script {eval_script}"

    # Run the evaluation script
    try:
        # We pass the output path just in case the script accepts it, 
        # but also run it without args if it fails.
        cmd = [sys.executable, eval_script]
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Evaluation script failed to run:\n{e.output}")

    # Extract the MSE value from the script's output
    # Matches floating point numbers including scientific notation
    floats = re.findall(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?", out)
    assert floats, f"Could not parse any numerical MSE value from the evaluation script output:\n{out}"

    # Assume the last number printed is the MSE
    mse = float(floats[-1])
    threshold = 1e-10

    assert mse <= threshold, f"Precision issue not fully fixed. MSE is {mse}, which is > threshold {threshold}"