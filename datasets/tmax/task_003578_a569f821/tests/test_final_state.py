# test_final_state.py

import os
import pytest

PIPELINE_DIR = "/home/user/pipeline"

def test_mse_txt():
    mse_path = os.path.join(PIPELINE_DIR, "mse.txt")
    assert os.path.isfile(mse_path), f"File {mse_path} does not exist."
    with open(mse_path, "r") as f:
        val = f.read().strip()
    try:
        mse_val = float(val)
    except ValueError:
        pytest.fail(f"mse.txt does not contain a valid float: {val}")

    assert mse_val == 0.0, f"Expected MSE to be 0.0, but got {mse_val}"

def test_correlation_txt():
    corr_path = os.path.join(PIPELINE_DIR, "correlation.txt")
    assert os.path.isfile(corr_path), f"File {corr_path} does not exist."
    with open(corr_path, "r") as f:
        val = f.read().strip()
    try:
        corr_val = float(val)
    except ValueError:
        pytest.fail(f"correlation.txt does not contain a valid float: {val}")

    assert corr_val == 0.0076, f"Expected correlation to be exactly 0.0076, but got {corr_val}"

def test_run_pipeline_sh():
    sh_path = os.path.join(PIPELINE_DIR, "run_pipeline.sh")
    assert os.path.isfile(sh_path), f"File {sh_path} does not exist."

    with open(sh_path, "r") as f:
        content = f.read()

    assert "etl.py" in content, "run_pipeline.sh does not appear to run etl.py"
    assert "analysis.py" in content, "run_pipeline.sh does not appear to run analysis.py"
    assert "score.py" in content, "run_pipeline.sh does not appear to run score.py"

def test_processed_csv_precision():
    csv_path = os.path.join(PIPELINE_DIR, "processed.csv")
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip().split(',') for line in f.readlines() if line.strip()]

    assert len(lines) >= 5, "processed.csv does not contain the expected number of rows."

    try:
        user_id_idx = lines[0].index("user_id")
        feature_2_idx = lines[0].index("feature_2")
    except ValueError:
        pytest.fail("processed.csv is missing 'user_id' or 'feature_2' in the header.")

    expected_f2 = {
        "1": "9007199254740993",
        "2": "0",
        "3": "9007199254740995",
        "4": "0"
    }

    for row in lines[1:]:
        uid = row[user_id_idx]
        f2_str = row[feature_2_idx]
        if uid in expected_f2:
            expected_val = expected_f2[uid]
            # If precision is preserved, the output string shouldn't be in scientific notation 
            # and should match the exact integer value (potentially with a '.0' if float but exact, 
            # though Int64 avoids '.0').
            assert f2_str == expected_val or f2_str == f"{expected_val}.0", \
                f"Precision lost or incorrect value for user {uid}. Expected {expected_val}, got {f2_str}"