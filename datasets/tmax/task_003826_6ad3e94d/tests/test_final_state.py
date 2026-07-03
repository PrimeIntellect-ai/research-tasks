# test_final_state.py

import os
import csv
import pytest

def test_results_file_exists():
    results_file = "/home/user/results.txt"
    assert os.path.exists(results_file), f"Output file {results_file} does not exist. Did you run the script?"
    assert os.path.isfile(results_file), f"{results_file} is not a file."

def test_results_content():
    metrics_file = "/home/user/metrics.csv"
    assert os.path.exists(metrics_file), f"{metrics_file} is missing."

    total_cpu = 0.0
    total_mem = 0.0
    count = 0

    with open(metrics_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            cpu = float(row["cpu_usage"])
            mem = float(row["mem_usage"])

            if abs(cpu - 99.9) < 1e-9:
                cpu = 100.0

            total_cpu += cpu
            total_mem += mem
            count += 1

    assert count > 0, "No data found in metrics.csv"

    expected_avg_cpu = total_cpu / count
    expected_avg_mem = total_mem / count

    expected_cpu_str = f"{expected_avg_cpu:.3f}"
    expected_mem_str = f"{expected_avg_mem:.3f}"

    results_file = "/home/user/results.txt"
    with open(results_file, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) >= 2, f"Expected at least 2 lines in {results_file}, got {len(content)}"

    cpu_line = content[0].strip()
    mem_line = content[1].strip()

    assert cpu_line.startswith("AvgCPU:"), f"First line must start with 'AvgCPU:', got '{cpu_line}'"
    assert mem_line.startswith("AvgMem:"), f"Second line must start with 'AvgMem:', got '{mem_line}'"

    actual_cpu_str = cpu_line.split(":", 1)[1].strip()
    actual_mem_str = mem_line.split(":", 1)[1].strip()

    assert actual_cpu_str == expected_cpu_str, f"Expected AvgCPU to be {expected_cpu_str}, got {actual_cpu_str}"
    assert actual_mem_str == expected_mem_str, f"Expected AvgMem to be {expected_mem_str}, got {actual_mem_str}"