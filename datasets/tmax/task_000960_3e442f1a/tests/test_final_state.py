# test_final_state.py

import os
import json
import re

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_perf.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist. You must create it."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable. Use 'chmod +x' to make it executable."

def test_results_json_exists_and_correct():
    json_path = "/home/user/results.json"
    assert os.path.isfile(json_path), f"Results file {json_path} does not exist. Did you run the script?"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} does not contain valid JSON."

    log_file = "/home/user/perf_logs.txt"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    x_vals = []
    y_vals = []
    with open(log_file, "r") as f:
        for line in f:
            if "load:" in line and "latency:" in line:
                m_load = re.search(r"load:([\d.]+)", line)
                m_lat = re.search(r"latency:([\d.]+)", line)
                if m_load and m_lat:
                    x_vals.append(float(m_load.group(1)))
                    y_vals.append(float(m_lat.group(1)))

    n = len(x_vals)
    assert n > 0, "No valid data points found in log file."

    sum_x = sum(x_vals)
    sum_y = sum(y_vals)
    sum_x2 = sum(x**2 for x in x_vals)
    sum_xy = sum(x*y for x, y in zip(x_vals, y_vals))

    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    b = (sum_y - m * sum_x) / n

    mean_y = sum_y / n
    null_mse = sum((y - mean_y)**2 for y in y_vals) / n
    model_mse = sum((y - (m * x + b))**2 for x, y in zip(x_vals, y_vals)) / n

    expected_m = f"{m:.2f}"
    expected_b = f"{b:.2f}"
    expected_model_mse = f"{abs(model_mse):.2f}"  # avoid -0.00
    expected_null_mse = f"{null_mse:.2f}"

    assert "m" in data, "Key 'm' missing in JSON output."
    assert "b" in data, "Key 'b' missing in JSON output."
    assert "model_mse" in data, "Key 'model_mse' missing in JSON output."
    assert "null_mse" in data, "Key 'null_mse' missing in JSON output."

    assert str(data["m"]) == expected_m, f"Expected m='{expected_m}', got '{data['m']}'"
    assert str(data["b"]) == expected_b, f"Expected b='{expected_b}', got '{data['b']}'"
    assert str(data["model_mse"]) == expected_model_mse, f"Expected model_mse='{expected_model_mse}', got '{data['model_mse']}'"
    assert str(data["null_mse"]) == expected_null_mse, f"Expected null_mse='{expected_null_mse}', got '{data['null_mse']}'"