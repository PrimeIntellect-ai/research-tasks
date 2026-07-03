# test_final_state.py

import os
import sqlite3
import pytest
import requests
import numpy as np
import cv2
import pandas as pd

def get_expected_data():
    """Recompute the expected imputed and rolling average values."""
    y_coords = []
    for t in range(50):
        frame = np.zeros((64, 64), dtype=np.uint8)
        y = int(30 + 20 * np.sin(0.2 * t))
        x = 32

        if t not in [10, 11, 25]:
            cv2.circle(frame, (x, y), 2, 255, -1)
            if frame.max() >= 100:
                y_brightest = np.argmax(frame) // 64
                y_coords.append(float(y_brightest))
            else:
                y_coords.append(np.nan)
        else:
            y_coords.append(np.nan)

    s = pd.Series(y_coords)
    s_imputed = s.interpolate(method='linear')
    s_rolling = s_imputed.rolling(window=5, center=True).mean()
    return s_imputed, s_rolling

@pytest.fixture(scope="module")
def expected_data():
    return get_expected_data()

def test_database_exists():
    """Test that the SQLite database exists at the expected location."""
    db_path = '/home/user/tracking.db'
    assert os.path.isfile(db_path), f"Database file is missing at {db_path}"

def test_database_schema():
    """Test that the trajectory table exists with the correct schema."""
    db_path = '/home/user/tracking.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trajectory';")
    table = cursor.fetchone()
    assert table is not None, "Table 'trajectory' does not exist in the database."

    cursor.execute("PRAGMA table_info(trajectory);")
    columns = {row[1]: row[2] for row in cursor.fetchall()}

    assert 'frame' in columns, "Column 'frame' missing from trajectory table."
    assert 'y_imputed' in columns, "Column 'y_imputed' missing from trajectory table."
    assert 'y_rolling_avg' in columns, "Column 'y_rolling_avg' missing from trajectory table."

    conn.close()

def test_api_valid_frame(expected_data):
    """Test the API for a valid frame (e.g., frame=5)."""
    s_imputed, s_rolling = expected_data
    frame_idx = 5

    url = f"http://127.0.0.1:8000/api/stats?frame={frame_idx}"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "frame" in data, "Response JSON missing 'frame' key."
    assert "y_imputed" in data, "Response JSON missing 'y_imputed' key."
    assert "y_rolling_avg" in data, "Response JSON missing 'y_rolling_avg' key."

    assert data["frame"] == frame_idx, f"Expected frame {frame_idx}, got {data['frame']}"

    expected_imputed = s_imputed.iloc[frame_idx]
    expected_rolling = s_rolling.iloc[frame_idx]

    assert np.isclose(data["y_imputed"], expected_imputed, atol=0.1), \
        f"Expected y_imputed ~{expected_imputed}, got {data['y_imputed']}"
    assert np.isclose(data["y_rolling_avg"], expected_rolling, atol=0.1), \
        f"Expected y_rolling_avg ~{expected_rolling}, got {data['y_rolling_avg']}"

def test_api_imputed_frame(expected_data):
    """Test the API for a frame that was originally missing (e.g., frame=10)."""
    s_imputed, s_rolling = expected_data
    frame_idx = 10

    url = f"http://127.0.0.1:8000/api/stats?frame={frame_idx}"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()

    expected_imputed = s_imputed.iloc[frame_idx]
    expected_rolling = s_rolling.iloc[frame_idx]

    assert np.isclose(data["y_imputed"], expected_imputed, atol=0.1), \
        f"Expected y_imputed ~{expected_imputed}, got {data['y_imputed']}"
    assert np.isclose(data["y_rolling_avg"], expected_rolling, atol=0.1), \
        f"Expected y_rolling_avg ~{expected_rolling}, got {data['y_rolling_avg']}"

def test_api_not_found():
    """Test the API for a frame that does not exist."""
    url = "http://127.0.0.1:8000/api/stats?frame=999"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 404, f"Expected status code 404 for missing frame, got {response.status_code}"