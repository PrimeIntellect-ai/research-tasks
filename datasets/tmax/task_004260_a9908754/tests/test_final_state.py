# test_final_state.py

import os
import subprocess
import json
import math
import pytest
import requests

def test_makefile_fixed():
    makefile_path = "/app/fastsim-2.0.0/Makefile"
    assert os.path.isfile(makefile_path), f"The file {makefile_path} is missing."

    with open(makefile_path, "r") as f:
        content = f.read()
        assert "-ffast-math" not in content, "The Makefile still contains the -ffast-math flag. It must be removed to fix the Kahan summation."

def test_dataset_exists():
    dataset_path = "/home/user/dataset.csv"
    assert os.path.isfile(dataset_path), f"The dataset file {dataset_path} is missing."

def test_metrics_endpoint():
    try:
        response = requests.get("http://127.0.0.1:8000/metrics", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at 127.0.0.1:8000/metrics: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail("The response from /metrics is not valid JSON.")

    expected_keys = {"analytical_slope", "bootstrap_ci_lower", "bootstrap_ci_upper"}
    assert set(data.keys()) == expected_keys, f"Expected JSON keys {expected_keys}, got {set(data.keys())}"

    # We will derive the expected values by compiling the fixed code and running the logic.
    # To be robust, we write a quick python script to get the exact expected values.
    # Since we can't reliably compile and run C++ in the test environment if the student modified it weirdly,
    # we will use the known correct values derived from the deterministic logic.
    # Actually, the prompt says "Treat truth as the intent... derive or recompute it in test code".
    # Let's write the C++ code, compile it, and generate the truth data.

    truth_cpp = """
#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>

int main(int argc, char** argv) {
    int n = 500;
    std::cout << "x,y\\n";
    for(int i=0; i<n; ++i) {
        double x = i * 0.1;
        double sum = 0.0;
        double c = 0.0;
        for(int j=1; j<=10000; ++j) {
            double y_val = (std::sin(x + j) / (j * j)) - c;
            double t = sum + y_val;
            c = (t - sum) - y_val;
            sum = t;
        }
        double y = 2.5 * x + 1.2 + sum;
        std::cout << std::fixed << std::setprecision(8) << x << "," << y << "\\n";
    }
    return 0;
}
"""
    with open("/tmp/truth_generator.cpp", "w") as f:
        f.write(truth_cpp)

    subprocess.run(["g++", "-O3", "-std=c++17", "/tmp/truth_generator.cpp", "-o", "/tmp/truth_generate_data"], check=True)

    result = subprocess.run(["/tmp/truth_generate_data"], capture_output=True, text=True, check=True)

    lines = result.stdout.strip().split("\n")
    assert lines[0] == "x,y"

    x_vals = []
    y_vals = []
    for line in lines[1:]:
        x_str, y_str = line.split(",")
        x_vals.append(float(x_str))
        y_vals.append(float(y_str))

    # Compute analytical slope
    n = len(x_vals)
    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n

    cov_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals)) / n
    var_x = sum((x - mean_x) ** 2 for x in x_vals) / n
    analytical_slope = cov_xy / var_x

    # Bootstrap
    import random
    random.seed(42)
    slopes = []
    for _ in range(2000):
        indices = [random.randint(0, n - 1) for _ in range(n)]
        x_b = [x_vals[i] for i in indices]
        y_b = [y_vals[i] for i in indices]

        m_x = sum(x_b) / n
        m_y = sum(y_b) / n
        c_xy = sum((x - m_x) * (y - m_y) for x, y in zip(x_b, y_b)) / n
        v_x = sum((x - m_x) ** 2 for x in x_b) / n
        slopes.append(c_xy / v_x)

    slopes.sort()

    def percentile(data_sorted, p):
        k = (len(data_sorted) - 1) * (p / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return data_sorted[int(k)]
        d0 = data_sorted[int(f)] * (c - k)
        d1 = data_sorted[int(c)] * (k - f)
        return d0 + d1

    # numpy percentile uses linear interpolation by default
    ci_lower = percentile(slopes, 2.5)
    ci_upper = percentile(slopes, 97.5)

    assert math.isclose(data["analytical_slope"], analytical_slope, rel_tol=1e-4, abs_tol=1e-4), f"Expected analytical_slope ~ {analytical_slope}, got {data['analytical_slope']}"
    assert math.isclose(data["bootstrap_ci_lower"], ci_lower, rel_tol=1e-4, abs_tol=1e-4), f"Expected bootstrap_ci_lower ~ {ci_lower}, got {data['bootstrap_ci_lower']}"
    assert math.isclose(data["bootstrap_ci_upper"], ci_upper, rel_tol=1e-4, abs_tol=1e-4), f"Expected bootstrap_ci_upper ~ {ci_upper}, got {data['bootstrap_ci_upper']}"