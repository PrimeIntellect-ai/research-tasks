# test_final_state.py
import os
import math

def test_compute_metrics_cpp_exists():
    assert os.path.isfile("/home/user/compute_metrics.cpp"), "C++ source file /home/user/compute_metrics.cpp is missing."

def test_plot_data_py_exists():
    assert os.path.isfile("/home/user/plot_data.py"), "Python script /home/user/plot_data.py is missing."

def test_distributions_png_exists():
    assert os.path.isfile("/home/user/distributions.png"), "Plot image /home/user/distributions.png is missing."
    assert os.path.getsize("/home/user/distributions.png") > 0, "/home/user/distributions.png is empty."

def test_normalized_data_csv():
    csv_path = "/home/user/normalized_data.csv"
    assert os.path.isfile(csv_path), f"Normalized data file {csv_path} is missing."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {csv_path}, found {len(lines)}."

    for i, line in enumerate(lines):
        values = line.split(",")
        assert len(values) == 1000, f"Expected 1000 comma-separated values on line {i+1}, found {len(values)}."
        # Check if they are valid floats
        try:
            [float(v) for v in values]
        except ValueError:
            assert False, f"Non-float values found in {csv_path} on line {i+1}."

def test_kl_divergence_value():
    kl_path = "/home/user/kl_divergence.txt"
    assert os.path.isfile(kl_path), f"KL divergence file {kl_path} is missing."

    latency_path = "/home/user/latency_data.txt"
    assert os.path.isfile(latency_path), f"Input data file {latency_path} is missing."

    with open(latency_path, "r") as f:
        lines = f.readlines()

    assert len(lines) == 2, "Input data should have 2 lines."

    P_raw = [float(x) for x in lines[0].strip().split()]
    Q_raw = [float(x) for x in lines[1].strip().split()]

    dx = 0.1
    P_smooth = [x + 1e-9 for x in P_raw]
    Q_smooth = [x + 1e-9 for x in Q_raw]

    def trapz_integral(y, dx):
        return sum((y[i] + y[i+1]) / 2.0 for i in range(len(y)-1)) * dx

    P_area = trapz_integral(P_smooth, dx)
    Q_area = trapz_integral(Q_smooth, dx)

    P_norm = [x / P_area for x in P_smooth]
    Q_norm = [x / Q_area for x in Q_smooth]

    kl_integrand = [p * math.log(p / q) for p, q in zip(P_norm, Q_norm)]
    expected_kl = trapz_integral(kl_integrand, dx)

    expected_kl_str = f"KL: {expected_kl:.6f}"

    with open(kl_path, "r") as f:
        actual_kl_str = f.read().strip()

    assert actual_kl_str == expected_kl_str, f"Expected KL divergence output '{expected_kl_str}', but got '{actual_kl_str}'."