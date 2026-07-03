# test_final_state.py

import os
import csv
import json
import subprocess
import time
from collections import defaultdict
import pytest

def get_expected_top_20():
    valid_years = set()
    with open('/home/user/dataset/papers.csv', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 3:
                pid = int(parts[0])
                year = int(parts[2])
                if year >= 2015:
                    valid_years.add(pid)

    in_degrees = defaultdict(int)
    for pid in valid_years:
        in_degrees[pid] = 0

    with open('/home/user/dataset/citations.txt', 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                src, tgt = int(parts[0]), int(parts[1])
                if src in valid_years and tgt in valid_years:
                    in_degrees[tgt] += 1

    sorted_papers = sorted(in_degrees.items(), key=lambda x: (-x[1], x[0]))
    top_20 = sorted_papers[:20]

    with open('/home/user/dataset/metadata.json', 'r') as f:
        metadata = json.load(f)

    keyword_map = {item["id"]: item["keywords"] for item in metadata}

    expected_lines = []
    for pid, count in top_20:
        kws = ",".join(keyword_map.get(pid, []))
        expected_lines.append(f"ID:{pid} | CITATIONS:{count} | KEYWORDS:{kws}")

    return expected_lines

def test_executable_exists():
    assert os.path.isfile('/home/user/analyze'), "/home/user/analyze executable does not exist."
    assert os.access('/home/user/analyze', os.X_OK), "/home/user/analyze is not executable."

def test_output_file_correctness():
    output_path = '/home/user/top_papers.out'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    expected_lines = get_expected_top_20()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"

def test_execution_time():
    executable = '/home/user/analyze'

    # Run using /usr/bin/time to measure execution time
    result = subprocess.run(
        ['/usr/bin/time', '-f', '%e', executable],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Execution of {executable} failed. Stderr: {result.stderr}"

    # The time output is printed to stderr by /usr/bin/time
    time_output = result.stderr.strip().split('\n')[-1]

    try:
        execution_time = float(time_output)
    except ValueError:
        pytest.fail(f"Could not parse execution time from output: {time_output}")

    threshold = 0.5
    assert execution_time <= threshold, f"Execution time {execution_time}s exceeded the threshold of {threshold}s."