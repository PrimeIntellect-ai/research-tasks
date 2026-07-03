# test_final_state.py

import os
import numpy as np
import pytest

PIPELINE_DIR = "/home/user/pipeline"
CLEANED_DATA_PATH = os.path.join(PIPELINE_DIR, "cleaned_data.csv")
TRUTH_DATA_PATH = os.path.join(PIPELINE_DIR, ".truth_data.csv")
REPORT_PNG_PATH = os.path.join(PIPELINE_DIR, "report.png")

def test_cleaned_data_exists():
    assert os.path.isfile(CLEANED_DATA_PATH), f"Expected {CLEANED_DATA_PATH} to exist, but it does not."

def test_cleaned_data_mse():
    assert os.path.isfile(CLEANED_DATA_PATH), "Cannot compute MSE because cleaned_data.csv is missing."
    assert os.path.isfile(TRUTH_DATA_PATH), "Truth data missing."

    try:
        agent_data = np.loadtxt(CLEANED_DATA_PATH)
    except Exception as e:
        pytest.fail(f"Failed to load agent's cleaned_data.csv: {e}")

    try:
        truth_data = np.loadtxt(TRUTH_DATA_PATH)
    except Exception as e:
        pytest.fail(f"Failed to load truth data: {e}")

    assert agent_data.shape == truth_data.shape, f"Shape mismatch: agent data has shape {agent_data.shape}, truth has {truth_data.shape}."

    mse = np.mean((agent_data - truth_data)**2)
    threshold = 0.001

    assert mse <= threshold, f"MSE between cleaned_data.csv and truth data is {mse:.6f}, which exceeds the threshold of {threshold}."

def test_report_png_exists():
    assert os.path.isfile(REPORT_PNG_PATH), f"Expected {REPORT_PNG_PATH} to exist, but it does not. Ensure the reporting service script was fixed and run."