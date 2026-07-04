# test_final_state.py
import os
import json
import csv
import math

def lorenz(state):
    x, y, z = state
    sigma = 10.0
    rho = 28.0
    beta = 8.0/3.0
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]

def euler(dt, steps):
    state = [1.0, 1.0, 1.0]
    for _ in range(steps):
        d = lorenz(state)
        state = [state[i] + dt * d[i] for i in range(3)]
    return state

def rk4(dt, steps):
    state = [1.0, 1.0, 1.0]
    for _ in range(steps):
        k1 = lorenz(state)
        s2 = [state[i] + 0.5 * dt * k1[i] for i in range(3)]
        k2 = lorenz(s2)
        s3 = [state[i] + 0.5 * dt * k2[i] for i in range(3)]
        k3 = lorenz(s3)
        s4 = [state[i] + dt * k3[i] for i in range(3)]
        k4 = lorenz(s4)
        state = [state[i] + (dt / 6.0) * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(3)]
    return state

def test_virtual_environment():
    """Check that the virtual environment was created."""
    venv_python = '/home/user/env/bin/python'
    assert os.path.isfile(venv_python), f"Virtual environment Python executable not found at {venv_python}"

def test_script_exists():
    """Check that the script was created."""
    script_path = '/home/user/generate_data.py'
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

def test_results_json():
    """Check the contents of results.json."""
    results_path = '/home/user/results.json'
    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not a valid JSON file"

    expected = {
        "rk4_0.01": [round(x, 5) for x in rk4(0.01, 200)],
        "rk4_0.001": [round(x, 5) for x in rk4(0.001, 2000)],
        "euler_0.01": [round(x, 5) for x in euler(0.01, 200)]
    }

    for key in expected:
        assert key in data, f"Key '{key}' missing from results.json"
        for i in range(3):
            assert math.isclose(data[key][i], expected[key][i], abs_tol=1e-4), \
                f"Value mismatch for {key} at index {i}. Expected approx {expected[key][i]}, got {data[key][i]}"

def test_training_data_csv():
    """Check the contents of training_data.csv."""
    csv_path = '/home/user/training_data.csv'
    assert os.path.isfile(csv_path), f"CSV file not found at {csv_path}"

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 2001, f"Expected 2001 rows in CSV, found {len(rows)}"

    header = [col.strip() for col in rows[0]]
    assert header == ['t', 'x', 'y', 'z'], f"Expected header ['t', 'x', 'y', 'z'], got {header}"

    first_row = [float(val) for val in rows[1]]
    assert first_row == [0.0, 1.0, 1.0, 1.0], f"Expected first data row to be [0.0, 1.0, 1.0, 1.0], got {first_row}"

def test_attractor_plot():
    """Check that the attractor plot was generated."""
    plot_path = '/home/user/attractor.png'
    assert os.path.isfile(plot_path), f"Plot file not found at {plot_path}"
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty"