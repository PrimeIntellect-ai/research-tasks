# test_final_state.py
import os
import csv
from collections import Counter

def get_vector(text):
    counts = Counter(c.lower() for c in text if c.isalpha())
    return [counts[chr(ord('a') + i)] for i in range(26)]

def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def compute_expected_result(csv_path):
    data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((int(row['id']), get_vector(row['text'])))

    best_pair = None
    max_dot = -1

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            id1, v1 = data[i]
            id2, v2 = data[j]

            if id1 > id2:
                id1, id2 = id2, id1

            dp = dot_product(v1, v2)

            if dp > max_dot:
                max_dot = dp
                best_pair = (id1, id2)
            elif dp == max_dot:
                if id1 < best_pair[0] or (id1 == best_pair[0] and id2 < best_pair[1]):
                    best_pair = (id1, id2)

    return f"{best_pair[0]},{best_pair[1]},{max_dot}"

def test_c_source_file_exists():
    c_file = '/home/user/find_similar.c'
    assert os.path.exists(c_file), f"C source file {c_file} is missing."
    assert os.path.isfile(c_file), f"{c_file} is not a file."

def test_result_file_correctness():
    csv_file = '/home/user/math_texts.csv'
    result_file = '/home/user/result.txt'

    assert os.path.exists(csv_file), f"Input CSV {csv_file} is missing."
    assert os.path.exists(result_file), f"Output file {result_file} is missing."
    assert os.path.isfile(result_file), f"{result_file} is not a file."

    expected_result = compute_expected_result(csv_file)

    with open(result_file, 'r', encoding='utf-8') as f:
        actual_result = f.read().strip()

    assert actual_result == expected_result, f"Expected '{expected_result}' in {result_file}, but got '{actual_result}'."