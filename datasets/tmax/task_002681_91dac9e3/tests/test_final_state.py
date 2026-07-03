# test_final_state.py

import os
import json
import math

def compute_expected_log(raw_data):
    vals = {item["pos"]: item["val"] for item in raw_data}

    expected_lines = []

    for bin_idx in range(10):
        start = bin_idx * 100
        end = start + 99

        # Calculate TVD
        bin_vals = [vals[i] for i in range(start, end + 1)]
        sum_val = sum(bin_vals)

        tvd = 0.0
        n = len(bin_vals)
        for v in bin_vals:
            p_i = v / sum_val
            u_i = 1.0 / n
            tvd += abs(p_i - u_i)
        tvd *= 0.5

        if tvd > 0.15:
            # Split into two halves
            mid = start + 49
            bins_to_integrate = [(start, mid), (mid + 1, end)]
        else:
            bins_to_integrate = [(start, end)]

        for b_start, b_end in bins_to_integrate:
            integral = 0.0
            for i in range(b_start, b_end):
                integral += (vals[i] + vals[i + 1]) / 2.0
            expected_lines.append(f"{b_start} {b_end} {integral:.2f}")

    return "\n".join(expected_lines) + "\n"

def test_processed_scores_txt():
    raw_path = "/home/user/raw_data.json"
    processed_path = "/home/user/processed_scores.txt"

    assert os.path.isfile(processed_path), f"Missing required file: {processed_path}"

    with open(raw_path, "r") as f:
        raw_data = json.load(f)

    with open(processed_path, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) == len(raw_data), f"Expected {len(raw_data)} lines in {processed_path}, got {len(lines)}"

    for i, line in enumerate(lines):
        parts = line.strip().split()
        assert len(parts) == 2, f"Line {i+1} in {processed_path} does not have exactly 2 columns"
        assert int(parts[0]) == raw_data[i]["pos"], f"Position mismatch at line {i+1}"
        assert math.isclose(float(parts[1]), raw_data[i]["val"], rel_tol=1e-5), f"Value mismatch at line {i+1}"

def test_cpp_file_exists():
    cpp_path = "/home/user/analyze_flex.cpp"
    assert os.path.isfile(cpp_path), f"Missing required C++ source file: {cpp_path}"

def test_integrated_flexibility_log():
    raw_path = "/home/user/raw_data.json"
    log_path = "/home/user/integrated_flexibility.log"

    assert os.path.isfile(log_path), f"Missing required log file: {log_path}"

    with open(raw_path, "r") as f:
        raw_data = json.load(f)

    expected_log = compute_expected_log(raw_data)

    with open(log_path, "r") as f:
        actual_log = f.read()

    assert actual_log.strip() == expected_log.strip(), f"Content of {log_path} does not match expected output.\nExpected:\n{expected_log}\nActual:\n{actual_log}"