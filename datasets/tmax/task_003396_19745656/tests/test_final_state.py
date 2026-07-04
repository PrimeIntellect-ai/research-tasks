# test_final_state.py
import socket
import cv2
import numpy as np
import pytest

def kahan_mean(arr):
    sum_ = 0.0
    c = 0.0
    for x in arr:
        y = x - c
        t = sum_ + y
        c = (t - sum_) - y
        sum_ = t
    return sum_ / len(arr)

def kahan_var(arr, mean):
    sum_ = 0.0
    c = 0.0
    for x in arr:
        y = (x - mean)**2 - c
        t = sum_ + y
        c = (t - sum_) - y
        sum_ = t
    return sum_ / len(arr)

def get_expected_metrics():
    cap = cv2.VideoCapture('/app/binding_kinetics.mp4')
    intensities = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        intensities.append(np.mean(gray))
    cap.release()

    intensities = np.array(intensities, dtype=np.float64)
    m = kahan_mean(intensities)
    v = kahan_var(intensities, m)

    fft_vals = np.abs(np.fft.fft(intensities))
    fft_vals[0] = 0
    dom_idx = np.argmax(fft_vals)

    return f"{dom_idx},{v:.6f}"

def test_server_response():
    expected = get_expected_metrics()

    # Test multiple sequential requests
    for i in range(2):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect(('127.0.0.1', 9090))
            s.sendall(b"GET_METRICS\n")
            data = s.recv(1024).decode('utf-8').strip()
            s.close()
        except Exception as e:
            pytest.fail(f"Failed to connect or receive data on request {i+1}: {e}")

        assert data == expected, f"Request {i+1}: expected '{expected}', got '{data}'"