# test_final_state.py

import os
import stat
import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error

def test_run_pipeline_script_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable"

def test_correlation_file():
    corr_path = "/home/user/correlation.txt"
    assert os.path.isfile(corr_path), f"{corr_path} does not exist"
    with open(corr_path, "r") as f:
        content = f.read().strip()

    try:
        corr_value = float(content)
    except ValueError:
        assert False, f"Content of {corr_path} is not a valid float: '{content}'"

    assert -1.0 <= corr_value <= 1.0, f"Correlation value {corr_value} is out of bounds [-1.0, 1.0]"

def test_model_exists_and_meets_rmse_threshold():
    model_path = "/home/user/model.joblib"
    test_data_path = "/app/hidden_test_data.csv"

    assert os.path.isfile(model_path), f"Model file {model_path} does not exist. Did the pipeline trigger the training API?"
    assert os.path.isfile(test_data_path), f"Hidden test data {test_data_path} is missing."

    try:
        model = joblib.load(model_path)
    except Exception as e:
        assert False, f"Failed to load model from {model_path}: {e}"

    try:
        test_df = pd.read_csv(test_data_path)
        X_test = test_df[['age', 'income', 'activity_score']]
        y_test = test_df['target']
    except Exception as e:
        assert False, f"Failed to load or parse test data from {test_data_path}: {e}"

    try:
        preds = model.predict(X_test)
    except Exception as e:
        assert False, f"Model prediction failed: {e}"

    rmse = mean_squared_error(y_test, preds, squared=False)
    assert rmse <= 12.5, f"RMSE {rmse:.4f} is greater than threshold 12.5"