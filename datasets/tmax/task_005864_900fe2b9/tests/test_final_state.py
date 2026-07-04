# test_final_state.py

import os
import math

def test_workload_compiled():
    """Test that the workload executable has been compiled."""
    executable_path = "/home/user/workload"
    assert os.path.exists(executable_path), f"Executable {executable_path} is missing."
    assert os.path.isfile(executable_path), f"{executable_path} is not a file."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

def test_metrics_txt():
    """Test that metrics.txt exists and contains the correct 100 values."""
    metrics_path = "/home/user/metrics.txt"
    assert os.path.exists(metrics_path), f"File {metrics_path} is missing."

    with open(metrics_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 100, f"Expected exactly 100 lines in metrics.txt, found {len(lines)}."

    # Verify the values
    for i, line in enumerate(lines):
        expected_val = 100.0 + 10.0 * math.sin(i) + (i % 3)
        try:
            val = float(line)
        except ValueError:
            assert False, f"Line {i+1} in metrics.txt is not a valid float: {line}"

        # Checking with some tolerance for formatting differences
        assert abs(val - expected_val) < 1e-3, f"Line {i+1} expected ~{expected_val:.4f}, got {val}"

def test_analyze_c_exists():
    """Test that analyze.c exists."""
    analyze_path = "/home/user/analyze.c"
    assert os.path.exists(analyze_path), f"File {analyze_path} is missing."
    assert os.path.isfile(analyze_path), f"{analyze_path} is not a file."

def test_stats_log():
    """Test that stats.log exists and contains the exact expected output."""
    stats_path = "/home/user/stats.log"
    assert os.path.exists(stats_path), f"File {stats_path} is missing."

    # Recompute the expected values using the exact algorithm specified
    data = [100.0 + 10.0 * math.sin(i) + (i % 3) for i in range(100)]

    state = 42
    def my_rand():
        nonlocal state
        state = (state * 1103515245 + 12345) & 0xFFFFFFFF
        return (state // 65536) % 32768

    means = []
    for _ in range(10000):
        current_sum = 0.0
        for _ in range(100):
            index = my_rand() % 100
            current_sum += data[index]
        means.append(current_sum / 100.0)

    overall_mean = sum(means) / 10000.0
    sum_sq_diff = sum((m - overall_mean) ** 2 for m in means)
    stddev = math.sqrt(sum_sq_diff / 10000.0)

    means.sort()
    ci_lower = means[250]
    ci_upper = means[9750]

    expected_output = (
        f"Mean: {overall_mean:.4f}\n"
        f"StdDev: {stddev:.4f}\n"
        f"CI_Lower: {ci_lower:.4f}\n"
        f"CI_Upper: {ci_upper:.4f}\n"
    )

    with open(stats_path, "r") as f:
        actual_output = f.read()

    assert actual_output.strip() == expected_output.strip(), (
        f"Contents of {stats_path} do not match the expected output.\n"
        f"Expected:\n{expected_output}\n"
        f"Actual:\n{actual_output}"
    )