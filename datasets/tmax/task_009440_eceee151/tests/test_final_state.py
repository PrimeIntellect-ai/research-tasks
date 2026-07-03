# test_final_state.py

import os
import math
import pytest

def test_find_leak_script_exists_and_executable():
    script_path = '/home/user/find_leak.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_leak_report_content():
    report_path = '/home/user/leak_report.txt'
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    train_dir = '/home/user/artifacts/train'
    test_dir = '/home/user/artifacts/test'

    # Compute the actual closest pair to be robust
    def read_vector(filepath):
        with open(filepath, 'r') as f:
            return [float(line.strip()) for line in f if line.strip()]

    test_files = [f for f in os.listdir(test_dir) if f.startswith('test_') and f.endswith('.txt')]
    train_files = [f for f in os.listdir(train_dir) if f.startswith('train_') and f.endswith('.txt')]

    closest_pair = None
    min_dist = float('inf')

    for test_f in test_files:
        test_vec = read_vector(os.path.join(test_dir, test_f))
        for train_f in train_files:
            train_vec = read_vector(os.path.join(train_dir, train_f))

            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(test_vec, train_vec)))
            if dist < min_dist:
                min_dist = dist
                closest_pair = (test_f, train_f)

    assert min_dist < 0.05, "No pair found with L2 distance < 0.05 in the dataset."
    expected_content = f"{closest_pair[0]} {closest_pair[1]}"

    with open(report_path, 'r') as f:
        content = f.read().strip()

    # Allow for multiple spaces or newlines, but exactly those two words
    words = content.split()
    assert len(words) == 2, f"Expected exactly 2 words in {report_path}, found {len(words)}: {content}"
    assert words[0] == closest_pair[0], f"Expected test file {closest_pair[0]}, found {words[0]}"
    assert words[1] == closest_pair[1], f"Expected train file {closest_pair[1]}, found {words[1]}"