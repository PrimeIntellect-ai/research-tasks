# test_final_state.py
import os

def compute_expected_mse(filename, seed):
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')

    true_vals = []
    pred_vals = []
    for line in lines:
        if line.strip():
            t, p = map(float, line.split(','))
            true_vals.append(t)
            pred_vals.append(p)

    state = seed
    def lcg_rand():
        nonlocal state
        state = (state * 1103515245 + 12345) % 2147483648
        return state

    total_mse = 0.0
    for _ in range(1000):
        iter_sse = 0.0
        for _ in range(10000):
            idx = lcg_rand() % 10000
            diff = true_vals[idx] - pred_vals[idx]
            iter_sse += diff * diff
        total_mse += iter_sse / 10000.0

    return total_mse / 1000.0

def test_report_contents():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Missing required report file: {report_path}"

    run_a_mse = compute_expected_mse("/home/user/run_A.csv", 42)
    run_b_mse = compute_expected_mse("/home/user/run_B.csv", 42)

    expected_lines = [
        f"Run A Bootstrap MSE: {run_a_mse:.6f}",
        f"Run B Bootstrap MSE: {run_b_mse:.6f}"
    ]

    with open(report_path, 'r') as f:
        actual_lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(actual_lines) == 2, f"Expected exactly 2 lines in {report_path}, found {len(actual_lines)}"

    assert actual_lines[0] == expected_lines[0], f"Line 1 mismatch. Expected: '{expected_lines[0]}', Found: '{actual_lines[0]}'"
    assert actual_lines[1] == expected_lines[1], f"Line 2 mismatch. Expected: '{expected_lines[1]}', Found: '{actual_lines[1]}'"