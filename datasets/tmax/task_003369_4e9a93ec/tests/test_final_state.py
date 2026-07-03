# test_final_state.py
import math
import requests
import pytest

def generate_spectrum(x, y, z):
    spectrum = []
    for i in range(10):
        val = math.sin(x + i * 0.5) * math.exp(-y / 5.0) + z * (i / 10.0)
        spectrum.append(val)
    return spectrum

def check_optimization(target_x, target_y, target_z):
    spectrum = generate_spectrum(target_x, target_y, target_z)
    payload = ",".join(f"{v:.6f}" for v in spectrum)

    url = "http://127.0.0.1:8080/optimize"
    try:
        response = requests.post(url, data=payload, timeout=10)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to or read from the optimization service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    text = response.text.strip()
    parts = text.split(",")
    assert len(parts) == 3, f"Expected 3 comma-separated values (x,y,z), got: {text}"

    try:
        res_x, res_y, res_z = map(float, parts)
    except ValueError:
        pytest.fail(f"Failed to parse response as 3 floats: {text}")

    # Check accuracy
    dist = math.sqrt((res_x - target_x)**2 + (res_y - target_y)**2 + (res_z - target_z)**2)
    assert dist <= 0.2, f"Returned parameters ({res_x}, {res_y}, {res_z}) are too far from target ({target_x}, {target_y}, {target_z}). Distance: {dist}"

def test_optimization_case_1():
    check_optimization(2.0, 3.0, 4.0)

def test_optimization_case_2():
    check_optimization(5.5, 1.2, 8.9)

def test_optimization_case_3():
    check_optimization(9.0, 9.0, 1.0)