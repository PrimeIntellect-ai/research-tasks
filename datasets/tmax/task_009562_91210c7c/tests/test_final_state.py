# test_final_state.py
import os
import json
import pytest

WORKSPACE_DIR = "/home/user/workspace"
GROUND_TRUTH_PATH = os.path.join(WORKSPACE_DIR, "ground_truth.json")
SUMMARY_PATH = os.path.join(WORKSPACE_DIR, "summary.txt")
CLEANED_DATA_PATH = os.path.join(WORKSPACE_DIR, "cleaned_data.csv")
PREDICTIONS_PATH = os.path.join(WORKSPACE_DIR, "predictions.csv")
MODEL_PATH = os.path.join(WORKSPACE_DIR, "model.py")
INFER_PATH = os.path.join(WORKSPACE_DIR, "infer.py")

def test_required_files_exist():
    """Ensure all required output scripts and files exist."""
    missing_files = []
    for path in [CLEANED_DATA_PATH, PREDICTIONS_PATH, SUMMARY_PATH, MODEL_PATH, INFER_PATH]:
        if not os.path.isfile(path):
            missing_files.append(path)

    assert not missing_files, f"The following required files are missing: {', '.join(missing_files)}"

def test_summary_contents():
    """Validate the contents of summary.txt against the ground truth."""
    assert os.path.isfile(GROUND_TRUTH_PATH), f"Ground truth file missing at {GROUND_TRUTH_PATH}"
    assert os.path.isfile(SUMMARY_PATH), f"Summary file missing at {SUMMARY_PATH}"

    with open(GROUND_TRUTH_PATH, "r") as f:
        ground_truth = json.load(f)

    expected_valid_rows = ground_truth["VALID_ROWS"]
    expected_sum_preds = ground_truth["SUM_PREDICTIONS"]

    with open(SUMMARY_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in summary.txt, found {len(lines)}"

    valid_rows_line = lines[0]
    sum_preds_line = lines[1]

    assert valid_rows_line.startswith("VALID_ROWS:"), "First line must start with 'VALID_ROWS:'"
    assert sum_preds_line.startswith("SUM_PREDICTIONS:"), "Second line must start with 'SUM_PREDICTIONS:'"

    try:
        actual_valid_rows = int(valid_rows_line.split(":")[1].strip())
    except ValueError:
        pytest.fail("Could not parse integer from VALID_ROWS line.")

    try:
        actual_sum_preds = float(sum_preds_line.split(":")[1].strip())
    except ValueError:
        pytest.fail("Could not parse float from SUM_PREDICTIONS line.")

    assert actual_valid_rows == expected_valid_rows, (
        f"VALID_ROWS mismatch. Expected {expected_valid_rows}, got {actual_valid_rows}"
    )

    # Use a small tolerance for floating point comparison, though rounding to 4 decimals was requested
    assert abs(actual_sum_preds - expected_sum_preds) < 1e-4, (
        f"SUM_PREDICTIONS mismatch. Expected {expected_sum_preds}, got {actual_sum_preds}"
    )

def test_predictions_format():
    """Ensure predictions.csv has the correct header and number of rows."""
    assert os.path.isfile(PREDICTIONS_PATH), f"Predictions file missing at {PREDICTIONS_PATH}"
    assert os.path.isfile(GROUND_TRUTH_PATH), f"Ground truth file missing at {GROUND_TRUTH_PATH}"

    with open(GROUND_TRUTH_PATH, "r") as f:
        ground_truth = json.load(f)
    expected_valid_rows = ground_truth["VALID_ROWS"]

    with open(PREDICTIONS_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "predictions.csv is empty."
    header = lines[0]
    assert header == "prediction", f"Expected header 'prediction', got '{header}'"

    actual_rows = len(lines) - 1
    assert actual_rows == expected_valid_rows, (
        f"predictions.csv row count mismatch. Expected {expected_valid_rows}, got {actual_rows}"
    )

def test_cleaned_data_format():
    """Ensure cleaned_data.csv has the correct headers and number of rows."""
    assert os.path.isfile(CLEANED_DATA_PATH), f"Cleaned data file missing at {CLEANED_DATA_PATH}"
    assert os.path.isfile(GROUND_TRUTH_PATH), f"Ground truth file missing at {GROUND_TRUTH_PATH}"

    with open(GROUND_TRUTH_PATH, "r") as f:
        ground_truth = json.load(f)
    expected_valid_rows = ground_truth["VALID_ROWS"]

    with open(CLEANED_DATA_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "cleaned_data.csv is empty."
    header = lines[0]
    expected_header = "f1,f2,f3,f4,f5"
    assert header == expected_header, f"Expected header '{expected_header}', got '{header}'"

    actual_rows = len(lines) - 1
    assert actual_rows == expected_valid_rows, (
        f"cleaned_data.csv row count mismatch. Expected {expected_valid_rows}, got {actual_rows}"
    )