# test_final_state.py
import os
import math
from collections import defaultdict

def compute_expected_best_param(data_path, target=150.0):
    # Read data
    data = []
    with open(data_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            data.append((int(parts[0]), float(parts[1]), float(parts[2])))

    best_p = None
    best_score = None
    min_diff = float('inf')

    for p in [1, 2, 3, 4, 5]:
        sums = defaultdict(lambda: [0.0, 0.0])
        for row in data:
            uid, v1, v2 = row
            sums[uid][0] += v1 ** p
            sums[uid][1] += v2 ** p

        score = 0.0
        for uid, (s1, s2) in sums.items():
            score += math.sqrt(s1**2 + s2**2)

        diff = abs(score - target)
        if diff < min_diff:
            min_diff = diff
            best_p = p
            best_score = score

    return best_p, f"{best_score:.4f}"

def test_etl_processor_cpp_exists():
    path = "/home/user/etl_processor.cpp"
    assert os.path.isfile(path), f"C++ source code is missing at {path}"

def test_etl_processor_executable_exists():
    path = "/home/user/etl_processor"
    assert os.path.isfile(path), f"Compiled executable is missing at {path}"
    assert os.access(path, os.X_OK), f"File {path} is not executable"

def test_tune_sh_exists():
    path = "/home/user/tune.sh"
    assert os.path.isfile(path), f"Bash script is missing at {path}"

def test_best_param_txt_correct():
    path = "/home/user/best_param.txt"
    assert os.path.isfile(path), f"Output file is missing at {path}"

    data_path = "/home/user/data.csv"
    assert os.path.isfile(data_path), f"Input data file missing at {data_path}"

    best_p, best_score_str = compute_expected_best_param(data_path)
    expected_content = f"p={best_p},score={best_score_str}"

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {path} is '{content}', expected '{expected_content}'"