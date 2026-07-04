# test_final_state.py
import os
import json
import math
import pytest

def test_scripts_exist():
    """Check if the required Python scripts were created."""
    assert os.path.exists('/home/user/project/prepare.py'), "prepare.py is missing from /home/user/project/"
    assert os.path.exists('/home/user/project/train.py'), "train.py is missing from /home/user/project/"

def test_parquet_exists_and_types():
    """Check if the processed.parquet file exists and has the correct data types."""
    parquet_path = '/home/user/project/processed.parquet'
    assert os.path.exists(parquet_path), f"{parquet_path} does not exist. Did prepare.py run successfully?"

    try:
        import pandas as pd
    except ImportError:
        pytest.fail("pandas is not installed. The environment setup is incomplete.")

    try:
        df = pd.read_parquet(parquet_path)
    except Exception as e:
        pytest.fail(f"Failed to read {parquet_path}. Is it a valid parquet file? Error: {e}")

    # Check data types
    assert str(df['id'].dtype) == 'int64', f"id column is not strictly int64, got {df['id'].dtype}"
    assert str(df['user_id'].dtype) == 'int64', f"user_id column is not strictly int64, got {df['user_id'].dtype}"
    assert str(df['click_count'].dtype) == 'int64', f"click_count column is not strictly int64, got {df['click_count'].dtype}"

    # Check for missing values
    assert df['user_id'].isna().sum() == 0, "user_id column still contains missing values (NaNs)"
    assert df['click_count'].isna().sum() == 0, "click_count column still contains missing values (NaNs)"

def test_metrics_json_and_mse():
    """Check if metrics.json exists, is properly formatted, and contains the correct MSE."""
    metrics_path = '/home/user/project/metrics.json'
    assert os.path.exists(metrics_path), f"{metrics_path} does not exist. Did train.py run successfully?"

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{metrics_path} does not contain valid JSON.")

    assert "mse" in metrics, f"metrics.json must contain the key 'mse'. Got keys: {list(metrics.keys())}"
    actual_mse = metrics["mse"]
    assert isinstance(actual_mse, (float, int)), f"MSE value must be a float, got {type(actual_mse)}"

    # Compute expected MSE dynamically
    try:
        import pandas as pd
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import Ridge
        from sklearn.metrics import mean_squared_error
    except ImportError:
        pytest.fail("Required ML libraries (pandas, scikit-learn) are not installed.")

    raw_path = '/home/user/project/raw_features.csv'
    assert os.path.exists(raw_path), f"Original data {raw_path} is missing, cannot compute expected MSE."

    # Reference Implementation
    df = pd.read_csv(raw_path)
    df['user_id'] = df['user_id'].fillna(-1).astype('int64')
    df['click_count'] = df['click_count'].fillna(-1).astype('int64')
    df['id'] = df['id'].astype('int64')

    scaler = StandardScaler()
    df['time_spent'] = scaler.fit_transform(df[['time_spent']])

    X = df[['user_id', 'click_count', 'time_spent']]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

    model = Ridge(alpha=1.0, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    expected_mse = float(mean_squared_error(y_test, y_pred))

    assert math.isclose(actual_mse, expected_mse, rel_tol=1e-4, abs_tol=1e-4), \
        f"Computed MSE {actual_mse} does not match the expected MSE {expected_mse}."