# test_final_state.py
import os
import re
import csv

def test_analyze_c_exists_and_uses_time():
    c_file = '/home/user/analyze.c'
    assert os.path.isfile(c_file), f"C source file {c_file} is missing."
    with open(c_file, 'r') as f:
        content = f.read()
    assert '<time.h>' in content, "The C file does not include <time.h>."
    assert 'clock(' in content, "The C file does not use clock() for benchmarking."

def test_result_txt_correctness():
    csv_file = '/home/user/sensor_data.csv'
    result_file = '/home/user/result.txt'

    assert os.path.isfile(result_file), f"Result file {result_file} is missing."

    # Calculate truth
    total = 0
    count_f1 = 0
    count_f0 = 0

    s1_1_f1 = 0
    s2_0_f1 = 0
    s3_1_f1 = 0

    s1_1_f0 = 0
    s2_0_f0 = 0
    s3_1_f0 = 0

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            fault = int(row['fault'])
            s1 = int(row['s1'])
            s2 = int(row['s2'])
            s3 = int(row['s3'])

            if fault == 1:
                count_f1 += 1
                if s1 == 1: s1_1_f1 += 1
                if s2 == 0: s2_0_f1 += 1
                if s3 == 1: s3_1_f1 += 1
            else:
                count_f0 += 1
                if s1 == 1: s1_1_f0 += 1
                if s2 == 0: s2_0_f0 += 1
                if s3 == 1: s3_1_f0 += 1

    p_f1 = count_f1 / total
    p_f0 = count_f0 / total

    l_s1_f1 = (s1_1_f1 + 1) / (count_f1 + 2)
    l_s2_f1 = (s2_0_f1 + 1) / (count_f1 + 2)
    l_s3_f1 = (s3_1_f1 + 1) / (count_f1 + 2)

    l_s1_f0 = (s1_1_f0 + 1) / (count_f0 + 2)
    l_s2_f0 = (s2_0_f0 + 1) / (count_f0 + 2)
    l_s3_f0 = (s3_1_f0 + 1) / (count_f0 + 2)

    unnorm_f1 = p_f1 * l_s1_f1 * l_s2_f1 * l_s3_f1
    unnorm_f0 = p_f0 * l_s1_f0 * l_s2_f0 * l_s3_f0

    posterior_f1 = unnorm_f1 / (unnorm_f1 + unnorm_f0)
    expected_prob_str = f"Probability: {posterior_f1:.6f}"

    with open(result_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {result_file}, found {len(lines)}"

    assert lines[0] == expected_prob_str, f"Expected first line to be '{expected_prob_str}', got '{lines[0]}'"

    time_match = re.match(r"^Time: [0-9.]+ ms$", lines[1])
    assert time_match is not None, f"Expected second line to match 'Time: <Y> ms', got '{lines[1]}'"