# test_final_state.py

import os
import time
import json
import requests
import pytest
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def test_api_running_and_predicts_correctly():
    """
    Check if the API is running on port 5000 and returns the correct prediction.
    """
    # 1. Calculate the expected prediction
    csv_path = "/app/raw_housing_data.csv"
    assert os.path.exists(csv_path), f"Raw dataset missing at {csv_path}"

    df = pd.read_csv(csv_path)

    # Assume 80/20 split without shuffling (or standard train_test_split defaults)
    # To be robust against shuffle/no-shuffle, we compute the model on the first 80%
    # and also on the whole dataset, but the prompt implies a specific 80% split.
    # We will use the first 80% of rows as train data.
    train_size = int(len(df) * 0.8)
    train_df = df.iloc[:train_size].copy()

    # Apply transformations
    train_df['Area_t'] = train_df['Area'] * 0.95
    train_df['Age_t'] = (train_df['Age'] - 2) * 1.1

    scaler = StandardScaler()
    train_df['Income_t'] = scaler.fit_transform(train_df[['Income']])

    X_train = train_df[['Area_t', 'Age_t', 'Income_t']]
    y_train = train_df['Price']

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Target prediction
    target_area = 2000
    target_age = 5
    target_income = 80000

    test_area_t = target_area * 0.95
    test_age_t = (target_age - 2) * 1.1
    test_income_t = scaler.transform([[target_income]])[0][0]

    expected_price = model.predict([[test_area_t, test_age_t, test_income_t]])[0]

    # 2. Make request to the API
    url = "http://127.0.0.1:5000/predict"
    payload = {"Area": target_area, "Age": target_age, "Income": target_income}

    max_retries = 5
    response = None
    for i in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(1)

    assert response is not None, "API is not reachable at http://127.0.0.1:5000/predict"
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"API did not return valid JSON. Response text: {response.text}")

    assert "predicted_price" in data, f"Response JSON missing 'predicted_price' key. Got: {data}"

    actual_price = data["predicted_price"]
    assert isinstance(actual_price, (int, float)), "predicted_price must be a number"

    # We allow a relatively generous tolerance because the agent might have used train_test_split 
    # with a different random state, which slightly changes the trained model parameters.
    # A 5% relative tolerance should be safe for a linear model on 1000 rows.
    rel_error = abs(actual_price - expected_price) / abs(expected_price)
    assert rel_error < 0.05, (
        f"Predicted price {actual_price} is not close enough to expected {expected_price} "
        f"(relative error {rel_error:.4f} >= 0.05). Check ETL logic and split."
    )

def test_pid_file_exists():
    """Check if the PID file was created."""
    pid_file = "/app/api.pid"
    assert os.path.exists(pid_file), f"PID file is missing at {pid_file}"
    with open(pid_file, "r") as f:
        pid = f.read().strip()
    assert pid.isdigit(), f"PID file contains invalid PID: {pid}"