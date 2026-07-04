# test_final_state.py
import os
import math

def test_analysis_output_correctness():
    output_path = '/home/user/analysis_output.txt'
    csv_path = '/home/user/energy_signal.csv'

    assert os.path.isfile(output_path), f"Output file missing: {output_path}"
    assert os.path.isfile(csv_path), f"CSV file missing: {csv_path}"

    xs = []
    ys = []
    with open(csv_path, 'r') as f:
        header = next(f)
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(',')
            xs.append(float(parts[0]))
            ys.append(float(parts[1]))

    # 1. Compute Numerical Integral using Trapezoidal Rule
    integral = 0.0
    for i in range(1, len(xs)):
        dx = xs[i] - xs[i-1]
        integral += (ys[i-1] + ys[i]) / 2.0 * dx

    # 2. Compute Analytical Integral
    analytical = 10.0 * math.sin(10.0)

    # 3. Compute Integral Error
    error = abs(integral - analytical)

    # 4. Compute Max Derivative using Central Difference
    max_d = 0.0
    for i in range(1, len(xs)-1):
        dx2 = xs[i+1] - xs[i-1]
        d = abs(ys[i+1] - ys[i-1]) / dx2
        if d > max_d:
            max_d = d

    expected_lines = [
        f"Numerical Integral: {integral:.4f}",
        f"Analytical Integral: {analytical:.4f}",
        f"Integral Error: {error:.4f}",
        f"Max Derivative: {max_d:.4f}"
    ]

    with open(output_path, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == 4, f"Expected exactly 4 lines in {output_path}, got {len(actual_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual == expected, f"Mismatch on line {i+1}.\nExpected: '{expected}'\nActual:   '{actual}'"