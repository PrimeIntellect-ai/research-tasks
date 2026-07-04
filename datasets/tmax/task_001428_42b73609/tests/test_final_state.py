# test_final_state.py

import os
import pytest
import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error
import subprocess

def test_redis_status():
    """Verify that the agent successfully connected to Redis and set the status key."""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        status = r.get('pipeline_status')
        assert status == 'success', f"Expected Redis key 'pipeline_status' to be 'success', got {status}"
    except ImportError:
        # Fallback to redis-cli if the redis python package is not available to the test
        result = subprocess.run(['redis-cli', 'get', 'pipeline_status'], capture_output=True, text=True)
        assert result.returncode == 0, "Failed to connect to Redis using redis-cli."
        output = result.stdout.strip()
        assert 'success' in output, f"Expected Redis key 'pipeline_status' to contain 'success', got {output}"
    except Exception as e:
        pytest.fail(f"Redis connection or assertion failed: {e}")

def test_pipeline_evaluation_metric():
    """Verify that the final pipeline exists, is loadable, and achieves the required MAE on the hidden test set."""
    pipeline_path = '/home/user/final_pipeline.pkl'
    assert os.path.exists(pipeline_path), f"Final pipeline file not found at {pipeline_path}"

    try:
        pipeline = joblib.load(pipeline_path)
    except Exception as e:
        pytest.fail(f"Failed to load the pipeline from {pipeline_path} using joblib. Error: {e}")

    hidden_data_path = '/app/hidden_data.csv'
    assert os.path.exists(hidden_data_path), f"Hidden data file not found at {hidden_data_path}"

    hidden_df = pd.read_csv(hidden_data_path)

    # The pipeline should take raw inference data
    X_hidden = hidden_df[['description', 'category']]
    y_hidden = hidden_df['price']

    try:
        preds = pipeline.predict(X_hidden)
    except Exception as e:
        pytest.fail(f"Pipeline failed to predict on the hidden data. Ensure the pipeline handles raw data. Error: {e}")

    mae = mean_absolute_error(y_hidden, preds)

    # Assert against the threshold
    threshold = 45.0
    assert mae < threshold, f"Pipeline MAE on hidden test set is {mae:.2f}, which is not strictly less than the threshold of {threshold}."