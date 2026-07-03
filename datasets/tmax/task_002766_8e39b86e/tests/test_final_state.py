# test_final_state.py
import os
import json
import urllib.request
import urllib.parse
import pandas as pd
import joblib
from sklearn.metrics import r2_score

def test_model_exists():
    path = "/home/user/model.pkl"
    assert os.path.isfile(path), f"Model file {path} was not created."

def test_model_performance():
    path = "/home/user/model.pkl"
    assert os.path.isfile(path), f"Model file {path} is missing."

    test_df = pd.read_csv("/app/test_data.csv")
    X_test = test_df.drop(columns=['target'])
    y_test = test_df['target']

    try:
        pipeline = joblib.load(path)
    except Exception as e:
        assert False, f"Failed to load the model file at {path}: {e}"

    try:
        preds = pipeline.predict(X_test)
    except Exception as e:
        assert False, f"Failed to generate predictions using the loaded pipeline: {e}"

    score = r2_score(y_test, preds)
    assert score >= 0.75, f"R2 score {score:.4f} is below the required threshold of 0.75."

def test_mlflow_experiment_exists():
    experiment_name = "Feature_Engineering_Exp"
    url = f"http://localhost:5000/api/2.0/mlflow/experiments/get-by-name?experiment_name={urllib.parse.quote(experiment_name)}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            assert response.status == 200, f"Failed to query MLflow API. Status code: {response.status}"
            data = json.loads(response.read().decode())
            assert "experiment" in data, f"Experiment '{experiment_name}' not found in MLflow."
    except urllib.error.URLError as e:
        assert False, f"Could not connect to MLflow at localhost:5000. Is the service running? Error: {e}"
    except Exception as e:
        assert False, f"An error occurred while verifying the MLflow experiment: {e}"