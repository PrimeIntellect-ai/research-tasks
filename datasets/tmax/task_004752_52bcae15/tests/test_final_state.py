# test_final_state.py

import os
import json
import socket
import pytest
import requests
import numpy as np
from scipy.optimize import minimize

def compute_expected_pipeline(signal):
    # Import the installed module to use its denoise function
    try:
        import freq_optimizer
    except ImportError:
        pytest.fail("freq_optimizer package is not installed or cannot be imported.")

    denoised = freq_optimizer.denoise(signal)
    fft_vals = np.fft.fft(denoised)
    # Keep only the real magnitudes of the positive frequencies
    n = len(fft_vals)
    pos_freq_magnitudes = np.abs(fft_vals[:n//2 + (1 if n % 2 != 0 else 0)])

    def objective(alpha):
        target = 100 * np.exp(-alpha[0] * np.arange(len(pos_freq_magnitudes)))
        return np.mean((pos_freq_magnitudes - target) ** 2)

    res = minimize(objective, [1.0], method='Nelder-Mead')
    alpha_opt = res.x[0]
    smoothed = 100 * np.exp(-alpha_opt * np.arange(len(pos_freq_magnitudes)))
    return alpha_opt, smoothed.tolist()

def test_makefile_fixed():
    makefile_path = "/app/freq_optimizer-1.0/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-lm" in content, "Makefile does not contain '-lm'. The C-extension will fail to link the math library."

def test_package_installed_and_working():
    try:
        import freq_optimizer
    except ImportError as e:
        pytest.fail(f"Failed to import freq_optimizer: {e}")

    # Test numerical stability
    signal = np.array([0.0, 1e10, -1e10])
    try:
        out = freq_optimizer.denoise(signal)
        assert not np.any(np.isnan(out)), "Output contains NaN values."
    except Exception as e:
        pytest.fail(f"freq_optimizer.denoise raised an exception: {e}")

def test_http_api():
    signal = [1.0, 0.5, -0.2, -0.8, 0.1, 0.9, -0.4, 0.0]
    expected_alpha, expected_smoothed = compute_expected_pipeline(signal)

    headers = {"Authorization": "Bearer ML_SECRET_2024"}
    payload = {"signal": signal}

    try:
        resp = requests.post("http://127.0.0.1:8000/process", json=payload, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"HTTP request to port 8000 failed: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}. Body: {resp.text}"

    try:
        data = resp.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "alpha" in data, "Response JSON missing 'alpha' key."
    assert "smoothed_spectrum" in data, "Response JSON missing 'smoothed_spectrum' key."

    assert np.isclose(data["alpha"], expected_alpha, rtol=1e-3), f"Expected alpha ~{expected_alpha}, got {data['alpha']}"
    assert np.allclose(data["smoothed_spectrum"], expected_smoothed, rtol=1e-3), "Smoothed spectrum does not match expected values."

def test_tcp_api():
    signal = [1.0, 0.5, -0.2, -0.8, 0.1, 0.9, -0.4, 0.0]
    _, expected_smoothed = compute_expected_pipeline(signal)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(("127.0.0.1", 9000))

        # Send auth
        s.sendall(b"AUTH:ML_SECRET_2024\n")

        # Send payload
        payload_str = ",".join(map(str, signal)) + "\n"
        s.sendall(payload_str.encode("utf-8"))

        # Read response
        response = b""
        while b"\n" not in response:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

        s.close()
    except Exception as e:
        pytest.fail(f"TCP connection or communication failed: {e}")

    response_str = response.decode("utf-8").strip()
    assert response_str, "Received empty response from TCP server."

    try:
        actual_smoothed = [float(x) for x in response_str.split(",")]
    except ValueError:
        pytest.fail(f"TCP response could not be parsed as comma-separated floats: {response_str}")

    assert np.allclose(actual_smoothed, expected_smoothed, rtol=1e-3), "TCP response smoothed spectrum does not match expected values."