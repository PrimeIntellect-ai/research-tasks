# test_final_state.py

import os
import json
import csv
import math
import pytest

def read_csv(filepath):
    data = {'cpu': [], 'mem': [], 'net_in': [], 'net_out': []}
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['cpu'].append(float(row['CPU_Usage']))
            data['mem'].append(float(row['Memory_Usage']))
            data['net_in'].append(float(row['Network_In']))
            data['net_out'].append(float(row['Network_Out']))
    return data

def mean(lst):
    return sum(lst) / len(lst)

def pearson_corr(x, y):
    mean_x = mean(x)
    mean_y = mean(y)
    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = sum((xi - mean_x) ** 2 for xi in x)
    den_y = sum((yi - mean_y) ** 2 for yi in y)
    return num / math.sqrt(den_x * den_y)

def linreg_slope(x, y):
    mean_x = mean(x)
    mean_y = mean(y)
    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den = sum((xi - mean_x) ** 2 for xi in x)
    return num / den

def cos_sim(v1, v2):
    dot = sum(x * y for x, y in zip(v1, v2))
    norm1 = math.sqrt(sum(x * x for x in v1))
    norm2 = math.sqrt(sum(x * x for x in v2))
    return dot / (norm1 * norm2)

def test_results_json_exists():
    assert os.path.exists('/home/user/sysmetrics/results.json'), "The output file /home/user/sysmetrics/results.json was not found."

def test_results_json_content():
    results_file = '/home/user/sysmetrics/results.json'
    assert os.path.exists(results_file), "The output file /home/user/sysmetrics/results.json was not found."

    with open(results_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/sysmetrics/results.json is not valid JSON.")

    required_keys = ["correlation_A", "regression_slope_B", "cosine_similarity_AC"]
    for key in required_keys:
        assert key in results, f"Key '{key}' is missing from the JSON results."
        assert isinstance(results[key], (int, float)), f"Value for '{key}' must be a number."

    # Compute truth
    dataA = read_csv('/home/user/data/serverA.csv')
    dataB = read_csv('/home/user/data/serverB.csv')
    dataC = read_csv('/home/user/data/serverC.csv')

    corr_A = pearson_corr(dataA['cpu'], dataA['mem'])
    slope_B = linreg_slope(dataB['mem'], dataB['cpu'])

    vecA = [mean(dataA['cpu']), mean(dataA['mem']), mean(dataA['net_in']), mean(dataA['net_out'])]
    vecC = [mean(dataC['cpu']), mean(dataC['mem']), mean(dataC['net_in']), mean(dataC['net_out'])]
    cos_AC = cos_sim(vecA, vecC)

    expected_corr_A = round(corr_A, 4)
    expected_slope_B = round(slope_B, 4)
    expected_cos_AC = round(cos_AC, 4)

    assert math.isclose(results["correlation_A"], expected_corr_A, abs_tol=1e-4), \
        f"correlation_A is incorrect. Expected {expected_corr_A}, got {results['correlation_A']}."

    assert math.isclose(results["regression_slope_B"], expected_slope_B, abs_tol=1e-4), \
        f"regression_slope_B is incorrect. Expected {expected_slope_B}, got {results['regression_slope_B']}."

    assert math.isclose(results["cosine_similarity_AC"], expected_cos_AC, abs_tol=1e-4), \
        f"cosine_similarity_AC is incorrect. Expected {expected_cos_AC}, got {results['cosine_similarity_AC']}."