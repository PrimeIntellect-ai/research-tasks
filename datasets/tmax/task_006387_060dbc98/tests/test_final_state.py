# test_final_state.py
import os
import csv
import re

def test_tokenized_dataset():
    input_csv = "/home/user/equations.csv"
    output_tsv = "/home/user/tokenized_dataset.tsv"

    assert os.path.isfile(input_csv), f"Input file {input_csv} is missing."
    assert os.path.isfile(output_tsv), f"Output file {output_tsv} is missing."

    expected_rows = []
    total_equations = 0
    total_tokens = 0

    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row or len(row) < 2:
                continue
            eq_id = row[0]
            expression = ",".join(row[1:])

            # Tokenize
            # Allowed single chars: + - * / = ^ ( )
            # Alphanumeric sequences: [a-zA-Z0-9]+
            # Ignore spaces
            tokens = []
            i = 0
            while i < len(expression):
                char = expression[i]
                if char.isspace():
                    i += 1
                    continue
                if char in "+-*/=^()":
                    tokens.append(char)
                    i += 1
                elif char.isalnum():
                    start = i
                    while i < len(expression) and expression[i].isalnum():
                        i += 1
                    tokens.append(expression[start:i])
                else:
                    # If there's any other character, the rule says "A token is either...". 
                    # We'll just treat it as individual characters or skip.
                    # The prompt says strictly rules, so we can just append it as a single token or skip.
                    # Assuming valid input based on setup.
                    tokens.append(char)
                    i += 1

            tokens_str = " ".join(tokens)
            token_count = len(tokens)

            expected_rows.append(f"{eq_id}\t{tokens_str}\t{token_count}")
            total_equations += 1
            total_tokens += token_count

    with open(output_tsv, "r", encoding="utf-8") as f:
        actual_lines = [line.strip("\r\n") for line in f if line.strip("\r\n")]

    assert len(actual_lines) == len(expected_rows), f"Expected {len(expected_rows)} rows in TSV, got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"

def test_experiment_log():
    input_csv = "/home/user/equations.csv"
    log_file = "/home/user/experiment_log.txt"

    assert os.path.isfile(input_csv), f"Input file {input_csv} is missing."
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    total_equations = 0
    total_tokens = 0

    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row or len(row) < 2:
                continue
            expression = ",".join(row[1:])

            tokens = []
            i = 0
            while i < len(expression):
                char = expression[i]
                if char.isspace():
                    i += 1
                    continue
                if char in "+-*/=^()":
                    tokens.append(char)
                    i += 1
                elif char.isalnum():
                    start = i
                    while i < len(expression) and expression[i].isalnum():
                        i += 1
                    tokens.append(expression[start:i])
                else:
                    tokens.append(char)
                    i += 1

            total_equations += 1
            total_tokens += len(tokens)

    expected_log_line = f"Run_Tokens: {total_equations},{total_tokens}"

    with open(log_file, "r", encoding="utf-8") as f:
        lines = [line.strip("\r\n") for line in f if line.strip("\r\n")]

    assert len(lines) > 0, f"Log file {log_file} is empty."
    actual_last_line = lines[-1]

    assert actual_last_line == expected_log_line, f"Last line of log file mismatch.\nExpected: {expected_log_line}\nActual:   {actual_last_line}"