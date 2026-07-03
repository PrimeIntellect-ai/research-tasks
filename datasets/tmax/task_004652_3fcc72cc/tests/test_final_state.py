# test_final_state.py

import os
import cv2
import numpy as np
from scipy.integrate import solve_ivp
import requests
import pytest

def compute_expected_value(frame_idx: int, rtol: float) -> str:
    """Computes the expected golden value for a given frame and rtol."""
    video_path = '/app/experiment.mp4'
    assert os.path.exists(video_path), f"Video file {video_path} does not exist"

    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    cap.release()

    assert ret, f"Could not read frame {frame_idx} from video"

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Crop central 50%
    h, w = gray.shape
    crop = gray[h//4 : 3*h//4, w//4 : 3*w//4]

    # Mean intensity
    V = np.mean(crop)

    # ODE
    def ode(t, x):
        return -0.05 * x + 10 * np.exp(-t)

    res = solve_ivp(ode, [0, 5.0], [V], rtol=rtol, atol=1e-6)
    final_val = res.y[0][-1]

    return f"{final_val:.4f}"

def test_endpoint_frame_5():
    """Test the endpoint with frame=5 and rtol=1e-4."""
    frame_idx = 5
    rtol = 1e-4
    expected_body = compute_expected_value(frame_idx, rtol)

    try:
        response = requests.get(f"http://127.0.0.1:8080/feature?frame={frame_idx}&rtol={rtol}", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    actual_body = response.text.strip()
    assert actual_body == expected_body, f"Expected response body '{expected_body}', got '{actual_body}'"

def test_endpoint_frame_15():
    """Test the endpoint with frame=15 and rtol=1e-2."""
    frame_idx = 15
    rtol = 1e-2
    expected_body = compute_expected_value(frame_idx, rtol)

    try:
        response = requests.get(f"http://127.0.0.1:8080/feature?frame={frame_idx}&rtol={rtol}", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    actual_body = response.text.strip()
    assert actual_body == expected_body, f"Expected response body '{expected_body}', got '{actual_body}'"