# test_final_state.py

import io
import time
import requests
import pytest
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import Ridge

def test_pipeline_end_to_end():
    # 1. Generate test data
    np.random.seed(123)
    n_samples = 100
    df = pd.DataFrame({
        'feature_1': np.random.randn(n_samples),
        'feature_2': np.random.randn(n_samples) * 2 + 1,
        'category': np.random.choice(['A', 'B', 'C'], size=n_samples),
        'target': np.random.randn(n_samples) * 5
    })

    # 2. Compute expected results
    df_encoded = pd.get_dummies(df, columns=['category'])
    X = df_encoded.drop(columns=['target'])
    y = df_encoded['target']

    expected_corr = X.corr(method='pearson').to_dict()

    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    model = Ridge(alpha=1.0)
    cv_scores = cross_val_score(model, X, y, cv=kf, scoring='r2')
    expected_cv_score = float(cv_scores.mean())

    # 3. Wait for services to be ready
    session = requests.Session()
    max_retries = 5
    for _ in range(max_retries):
        try:
            # Just check if port 5001 is responding
            session.get('http://127.0.0.1:5001/')
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)

    # 4. Send POST request to Worker API
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')

    try:
        post_response = session.post(
            'http://127.0.0.1:5001/process',
            files={'file': ('test.csv', csv_bytes, 'text/csv')}
        )
        assert post_response.status_code == 200, f"Worker API POST /process failed with status {post_response.status_code}: {post_response.text}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to Worker API on port 5001.")

    # Give the worker a moment to save to Redis if it's async, though the prompt implies it's synchronous or fast
    time.sleep(1)

    # 5. Send GET request to Report API
    try:
        get_response = session.get('http://127.0.0.1:5002/report')
        assert get_response.status_code == 200, f"Report API GET /report failed with status {get_response.status_code}: {get_response.text}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to Report API on port 5002.")

    data = get_response.json()

    # 6. Validate response payload
    assert 'cv_score' in data, "Response JSON is missing 'cv_score'"
    assert 'correlation_matrix' in data, "Response JSON is missing 'correlation_matrix'"

    # Validate CV score
    actual_cv_score = data['cv_score']
    assert isinstance(actual_cv_score, (float, int)), f"Expected cv_score to be a number, got {type(actual_cv_score)}"
    assert abs(actual_cv_score - expected_cv_score) < 1e-4, f"cv_score mismatch. Expected {expected_cv_score}, got {actual_cv_score}. Check random_state=42 and Ridge(alpha=1.0)."

    # Validate correlation matrix
    actual_corr = data['correlation_matrix']
    assert isinstance(actual_corr, dict), "correlation_matrix should be a nested dictionary"

    for k1, v1 in expected_corr.items():
        assert k1 in actual_corr, f"Feature {k1} missing from correlation matrix"
        for k2, v2 in v1.items():
            assert k2 in actual_corr[k1], f"Feature {k2} missing from correlation matrix[{k1}]"
            actual_val = actual_corr[k1][k2]
            # Handle NaNs if any (though unlikely with this data)
            if pd.isna(v2):
                assert pd.isna(actual_val) or actual_val is None, f"Expected NaN for corr({k1}, {k2}), got {actual_val}"
            else:
                assert abs(actual_val - v2) < 1e-4, f"Correlation mismatch for {k1} and {k2}. Expected {v2}, got {actual_val}"