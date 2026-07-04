# test_final_state.py

import os
import csv
import math

def compute_expected_values(csv_path):
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        data = { 'F1': [], 'F2': [], 'F3': [], 'F4': [], 'T': [] }
        for row in reader:
            for col in data.keys():
                data[col].append(float(row[col]))

    n = len(data['T'])
    target = data['T']
    mean_T = sum(target) / n

    best_feature = None
    best_corr_abs = -1
    best_corr_val = 0
    best_w = 0
    best_b = 0

    features = ['F1', 'F2', 'F3', 'F4']
    for f in features:
        feature_data = data[f]
        mean_F = sum(feature_data) / n

        num = 0.0
        den_F = 0.0
        den_T = 0.0

        for i in range(n):
            diff_F = feature_data[i] - mean_F
            diff_T = target[i] - mean_T
            num += diff_F * diff_T
            den_F += diff_F ** 2
            den_T += diff_T ** 2

        corr = num / math.sqrt(den_F * den_T)

        if abs(corr) > best_corr_abs:
            best_corr_abs = abs(corr)
            best_corr_val = corr
            best_feature = f
            best_w = num / den_F
            best_b = mean_T - best_w * mean_F

    return best_feature, best_corr_val, best_w, best_b

def test_pipeline_cpp_exists():
    """Check if the C++ source file exists."""
    assert os.path.exists('/home/user/pipeline.cpp'), "The source file /home/user/pipeline.cpp is missing."

def test_pipeline_binary_exists():
    """Check if the compiled binary exists and is executable."""
    binary_path = '/home/user/pipeline'
    assert os.path.exists(binary_path), f"The compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

def test_etl_model_output():
    """Check if the output file matches the expected calculations."""
    output_path = '/home/user/etl_model_output.txt'
    csv_path = '/home/user/sensor_data.csv'

    assert os.path.exists(output_path), f"The output file {output_path} is missing."
    assert os.path.exists(csv_path), f"The dataset file {csv_path} is missing."

    best_feature, best_corr_val, best_w, best_b = compute_expected_values(csv_path)

    expected_output = (
        f"SelectedFeature: {best_feature}\n"
        f"Correlation: {best_corr_val:.4f}\n"
        f"Weight: {best_w:.4f}\n"
        f"Bias: {best_b:.4f}"
    )

    with open(output_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"Output mismatch.\nExpected:\n{expected_output}\n\nGot:\n{actual_output}"