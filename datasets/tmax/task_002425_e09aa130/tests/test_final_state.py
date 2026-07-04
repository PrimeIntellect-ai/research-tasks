# test_final_state.py
import socket
import os
import csv
import pytest

def test_model_weights_and_server():
    # 1. Read data.csv and compute min/max of first 80 rows
    data_file = "/home/user/data.csv"
    assert os.path.exists(data_file), "data.csv is missing"

    xs = []
    with open(data_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            xs.append(float(row["X"]))

    assert len(xs) == 100, "data.csv should have 100 rows"

    train_xs = xs[:80]
    expected_min = min(train_xs)
    expected_max = max(train_xs)

    # 2. Read model.weights
    weights_file = "/home/user/model.weights"
    assert os.path.exists(weights_file), "model.weights is missing"

    with open(weights_file, "r") as f:
        content = f.read().strip().split()

    assert len(content) >= 4, "model.weights should contain w, b, min, max"

    try:
        w = float(content[0])
        b = float(content[1])
        actual_min = float(content[2])
        actual_max = float(content[3])
    except ValueError:
        pytest.fail("Could not parse floats from model.weights")

    # 3. Verify min and max match the first 80 rows (no data leakage)
    assert abs(actual_min - expected_min) < 1e-4, f"Data leakage or incorrect min. Expected {expected_min}, got {actual_min}"
    assert abs(actual_max - expected_max) < 1e-4, f"Data leakage or incorrect max. Expected {expected_max}, got {actual_max}"

    # 4. Test the server
    test_x = 42.5
    expected_x_scaled = (test_x - actual_min) / (actual_max - actual_min)
    expected_y_pred = w * expected_x_scaled + b
    expected_response = f"{expected_y_pred:.4f}\n"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3.0)
        s.connect(("127.0.0.1", 9000))
        s.sendall(f"{test_x}\n".encode("utf-8"))
        response = s.recv(1024).decode("utf-8")
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect to server on port 9000 or receive data: {e}")

    assert response == expected_response, f"Server returned {repr(response)}, expected {repr(expected_response)}"