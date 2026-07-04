# test_final_state.py
import os
import re

def parse_fasta(filepath):
    lengths = []
    gc_ratios = []
    with open(filepath, 'r') as f:
        seq = ""
        for line in f:
            if line.startswith(">"):
                if seq:
                    lengths.append(len(seq))
                    gc_ratios.append((seq.count('G') + seq.count('C')) / len(seq))
                    seq = ""
            else:
                seq += line.strip()
        if seq:
            lengths.append(len(seq))
            gc_ratios.append((seq.count('G') + seq.count('C')) / len(seq))
    return lengths, gc_ratios

def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x2 = sum(xi * xi for xi in x)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    return slope, intercept

def test_regression_results():
    fasta_path = '/home/user/sequences.fasta'
    results_path = '/home/user/regression_results.txt'

    assert os.path.exists(results_path), f"The file {results_path} does not exist."
    assert os.path.isfile(results_path), f"{results_path} is not a valid file."

    with open(results_path, 'r') as f:
        content = f.read().strip()

    lines = content.split('\n')
    assert len(lines) == 2, f"Expected exactly 2 lines in {results_path}, but found {len(lines)}."

    slope_match = re.match(r'^slope:\s*(-?\d+\.\d{6})$', lines[0])
    intercept_match = re.match(r'^intercept:\s*(-?\d+\.\d{6})$', lines[1])

    assert slope_match, f"The first line of {results_path} is not correctly formatted. Expected 'slope: <value>' with 6 decimal places, got '{lines[0]}'."
    assert intercept_match, f"The second line of {results_path} is not correctly formatted. Expected 'intercept: <value>' with 6 decimal places, got '{lines[1]}'."

    user_slope = slope_match.group(1)
    user_intercept = intercept_match.group(1)

    # Compute ground truth
    lengths, gc_ratios = parse_fasta(fasta_path)
    expected_slope_val, expected_intercept_val = linear_regression(lengths, gc_ratios)

    expected_slope = f"{expected_slope_val:.6f}"
    expected_intercept = f"{expected_intercept_val:.6f}"

    assert user_slope == expected_slope, f"Calculated slope is incorrect. Expected {expected_slope}, got {user_slope}."
    assert user_intercept == expected_intercept, f"Calculated intercept is incorrect. Expected {expected_intercept}, got {user_intercept}."