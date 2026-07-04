import io
import requests
import pytest
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.stats import pearsonr

def test_api_analyze_endpoint():
    """
    Test the /api/analyze endpoint by sending a CSV and validating the mathematical results
    returned by the agent's service.
    """
    # Construct the test CSV data
    csv_content = """f1,f2,f3,f4,f5
10,,30,40,50
20,25,,45,55
30,35,40,,60
40,45,50,55,
,,60,65,70
"""

    # Calculate expected values locally
    # 1. Clean data based on rules
    df = pd.read_csv(io.StringIO(csv_content))
    for col in df.columns:
        median_val = df[col].median(skipna=True)
        # Round half to even
        median_rounded = np.round(median_val)
        df[col] = df[col].fillna(median_rounded).astype('int64')

    # 2. Oracle scores
    # Oracle formula: score = (f1 * 0.5) + (f2 * 2.0) - (f3 * 1.5) + (f4 * 0.1) - (f5 * 0.8)
    scores = (df['f1'] * 0.5) + (df['f2'] * 2.0) - (df['f3'] * 1.5) + (df['f4'] * 0.1) - (df['f5'] * 0.8)

    # 3. Correlation
    correlation_f3_score, _ = pearsonr(df['f3'], scores)

    # 4. PCA
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    pca = PCA(n_components=1)
    pc1 = pca.fit_transform(scaled_data).flatten()

    # 5. Confidence Interval
    n = len(pc1)
    mean_pc1 = np.mean(pc1)
    std_pc1 = np.std(pc1, ddof=1)
    margin_of_error = 1.96 * (std_pc1 / np.sqrt(n))
    ci_lower = mean_pc1 - margin_of_error
    ci_upper = mean_pc1 + margin_of_error

    # Send request to the API
    url = "http://127.0.0.1:8000/api/analyze"
    files = {"file": ("test.csv", csv_content, "text/csv")}

    try:
        response = requests.post(url, files=files, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    # Verify the keys
    expected_keys = {"correlation_f3_score", "pc1_mean_ci_lower", "pc1_mean_ci_upper"}
    actual_keys = set(data.keys())
    assert expected_keys.issubset(actual_keys), f"Missing keys in response. Expected {expected_keys}, got {actual_keys}"

    # Verify the values with tolerance
    tolerance = 0.001
    assert abs(data["correlation_f3_score"] - correlation_f3_score) <= tolerance, \
        f"correlation_f3_score mismatch. Expected ~{correlation_f3_score:.4f}, got {data['correlation_f3_score']}"

    assert abs(data["pc1_mean_ci_lower"] - ci_lower) <= tolerance, \
        f"pc1_mean_ci_lower mismatch. Expected ~{ci_lower:.4f}, got {data['pc1_mean_ci_lower']}"

    assert abs(data["pc1_mean_ci_upper"] - ci_upper) <= tolerance, \
        f"pc1_mean_ci_upper mismatch. Expected ~{ci_upper:.4f}, got {data['pc1_mean_ci_upper']}"