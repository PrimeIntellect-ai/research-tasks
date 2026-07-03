# test_final_state.py
import os
import pytest

def test_forecast_mse():
    """Test that the forecast.txt file exists, has 5 lines, and MSE <= 0.05"""
    target_values = [12.74, 14.64, 16.54, 18.44, 20.34]
    forecast_file = '/home/user/forecast.txt'

    assert os.path.exists(forecast_file), f"Expected forecast file at {forecast_file} does not exist."

    with open(forecast_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 numeric values in {forecast_file}, found {len(lines)}"

    try:
        predictions = [float(line) for line in lines]
    except ValueError as e:
        pytest.fail(f"Could not parse predictions as floats: {e}")

    mse = sum((pred - target)**2 for pred, target in zip(predictions, target_values)) / 5.0

    assert mse <= 0.05, f"MSE is {mse}, which is greater than the threshold of 0.05. Predictions: {predictions}"