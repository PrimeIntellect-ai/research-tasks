# test_final_state.py

import os
import re
import math
import pytest

def test_analyze_c_exists():
    assert os.path.exists("/home/user/analyze.c"), "The C source file /home/user/analyze.c is missing."
    assert os.path.isfile("/home/user/analyze.c"), "/home/user/analyze.c is not a regular file."

def test_run_pipeline_sh_exists_and_executable():
    path = "/home/user/run_pipeline.sh"
    assert os.path.exists(path), f"The bash script {path} is missing."
    assert os.path.isfile(path), f"{path} is not a regular file."
    assert os.access(path, os.X_OK), f"The script {path} is not executable."

def test_analysis_result():
    result_path = "/home/user/analysis_result.txt"
    assert os.path.exists(result_path), f"The output file {result_path} is missing."

    # Compute ground truth dynamically from reviews.csv
    csv_path = "/home/user/reviews.csv"
    assert os.path.exists(csv_path), f"Input file {csv_path} is missing."

    five_star_count = 0
    token_lengths = []

    with open(csv_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',', 2)
            if len(parts) == 3:
                rating = parts[1]
                text = parts[2]
                if rating == '5':
                    five_star_count += 1
                    # Tokenize with delimiters: space, tab, newline, period, comma, exclamation mark, question mark, semicolon, colon
                    tokens = re.split(r'[ \t\n.,!?;:]+', text)
                    for token in tokens:
                        if token:
                            token_lengths.append(len(token))

    total_tokens = len(token_lengths)

    if total_tokens > 0:
        mean = sum(token_lengths) / total_tokens
        if total_tokens > 1:
            variance = sum((x - mean) ** 2 for x in token_lengths) / (total_tokens - 1)
            std_dev = math.sqrt(variance)
        else:
            std_dev = 0.0

        margin_of_error = 1.96 * (std_dev / math.sqrt(total_tokens))
        lower_bound = mean - margin_of_error
        upper_bound = mean + margin_of_error
    else:
        mean = 0.0
        lower_bound = 0.0
        upper_bound = 0.0

    expected_output = (
        f"Total 5-star reviews: {five_star_count}\n"
        f"Total tokens in 5-star reviews: {total_tokens}\n"
        f"Mean token length: {mean:.4f}\n"
        f"95% CI: [{lower_bound:.4f}, {upper_bound:.4f}]"
    )

    with open(result_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"The content of {result_path} does not match the expected output.\n"
        f"Expected:\n{expected_output}\n\nActual:\n{actual_output}"
    )