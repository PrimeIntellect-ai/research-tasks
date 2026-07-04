# test_final_state.py
import os
import json
import pytest

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Expected output file {results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} is not valid JSON.")

    assert "valid_rows" in results, "Missing 'valid_rows' in results.json"
    assert "inference_sum" in results, "Missing 'inference_sum' in results.json"
    assert "benchmark_time_ms" in results, "Missing 'benchmark_time_ms' in results.json"

    # Compute expected values from the data files
    artifacts_path = "/home/user/data/artifacts.csv"
    weights_path = "/home/user/data/weights.txt"

    assert os.path.isfile(artifacts_path), f"Missing {artifacts_path} to compute truth."
    assert os.path.isfile(weights_path), f"Missing {weights_path} to compute truth."

    with open(weights_path, "r") as f:
        w_strs = f.read().strip().split(",")
        weights = [float(w) for w in w_strs]

    valid_rows = 0
    inference_sum = 0.0

    with open(artifacts_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cols = line.split(",")
            if len(cols) != 5:
                continue

            id_str, count_str, f1_str, f2_str, f3_str = cols

            # Rule 1: id must be a valid integer
            try:
                int(id_str)
            except ValueError:
                continue

            # Rule 2: count must be an integer, impute empty/NaN to 0, drop if contains decimal
            if count_str == "" or count_str == "NaN":
                count = 0
            elif "." in count_str:
                continue
            else:
                try:
                    count = int(count_str)
                except ValueError:
                    continue

            # Rule 3: f1, f2, f3 must be floats, impute empty/NaN to 0.0
            def parse_float(val_str):
                if val_str == "" or val_str == "NaN":
                    return 0.0
                return float(val_str)

            try:
                f1 = parse_float(f1_str)
                f2 = parse_float(f2_str)
                f3 = parse_float(f3_str)
            except ValueError:
                continue

            valid_rows += 1

            # Calculate inference result for the row
            y = count * weights[0] + f1 * weights[1] + f2 * weights[2] + f3 * weights[3]
            inference_sum += y

    assert results["valid_rows"] == valid_rows, f"Expected valid_rows to be {valid_rows}, got {results['valid_rows']}."
    assert abs(results["inference_sum"] - inference_sum) < 1e-3, f"Expected inference_sum approx {inference_sum:.4f}, got {results['inference_sum']}."
    assert isinstance(results["benchmark_time_ms"], (int, float)), "benchmark_time_ms must be a number."
    assert results["benchmark_time_ms"] > 0, "benchmark_time_ms must be greater than 0."