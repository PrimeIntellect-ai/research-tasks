# test_final_state.py
import os
import math

def test_results_file_exists_and_correct():
    path = '/home/user/results.txt'
    assert os.path.exists(path), f"File {path} does not exist. The C++ program must generate this file."

    with open(path, 'r') as f:
        content = f.read().strip()

    lines = content.split('\n')
    assert len(lines) >= 2, f"Expected at least 2 lines in {path}, got {len(lines)}."

    # Parse the output
    results = {}
    for line in lines:
        if ':' in line:
            key, val = line.split(':', 1)
            results[key.strip()] = val.strip()

    assert 't_stat' in results, "Missing 't_stat' in results.txt"
    assert 'jc_p' in results, "Missing 'jc_p' in results.txt"

    # Expected values derived from the sequences
    # seqA: [0.5, 0.0, 1.0, 0.5, 0.5] -> Mean A = 0.5, Var A = 0.125
    # seqB: [1.0, 1.0, 0.5, 1.0, 1.0] -> Mean B = 0.9, Var B = 0.05
    # t = (0.5 - 0.9) / sqrt(0.125/5 + 0.05/5) = -0.4 / sqrt(0.035) = -2.138089935
    # d = 0.4
    # p = 0.75 * (1 - exp(-4/3 * 0.4)) = 0.310015

    expected_t_stat = "-2.1381"
    expected_jc_p = "0.3100"

    assert results['t_stat'] == expected_t_stat, f"Expected t_stat to be {expected_t_stat}, got {results['t_stat']}"
    assert results['jc_p'] == expected_jc_p, f"Expected jc_p to be {expected_jc_p}, got {results['jc_p']}"

def test_cpp_file_exists():
    path = '/home/user/analyze.cpp'
    assert os.path.exists(path), f"Source file {path} is missing."