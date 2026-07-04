# test_final_state.py

import os
import re
import math
import subprocess
import pytest

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z]', ' ', text)
    return text.split()

def compute_expected_scores(domain_path, generic_path, target_path):
    with open(domain_path, 'r') as f:
        domain_text = f.read()
    with open(generic_path, 'r') as f:
        generic_text = f.read()
    with open(target_path, 'r') as f:
        target_lines = f.readlines()

    domain_words = tokenize(domain_text)
    generic_words = tokenize(generic_text)

    n_domain = len(domain_words)
    n_generic = len(generic_words)

    vocab = set(domain_words).union(set(generic_words))
    v = len(vocab)

    domain_counts = {}
    for w in domain_words:
        domain_counts[w] = domain_counts.get(w, 0) + 1

    generic_counts = {}
    for w in generic_words:
        generic_counts[w] = generic_counts.get(w, 0) + 1

    expected_output = []
    for i, line in enumerate(target_lines, 1):
        words = tokenize(line)
        score = 0.0
        for w in words:
            c_d = domain_counts.get(w, 0)
            c_g = generic_counts.get(w, 0)

            p_d = (c_d + 1) / (n_domain + v)
            p_g = (c_g + 1) / (n_generic + v)

            score += math.log(p_d) - math.log(p_g)

        classification = "DOMAIN" if score > 0 else "GENERIC"
        expected_output.append(f"{i}\t{score:.4f}\t{classification}")

    return expected_output

def test_script_exists_and_executable():
    script_path = "/home/user/filter_dataset.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_output_correctness():
    script_path = "/home/user/filter_dataset.sh"
    domain_path = "/home/user/domain.txt"
    generic_path = "/home/user/generic.txt"
    target_path = "/home/user/target.txt"
    output_path = "/home/user/scores.tsv"

    # Remove previous output if exists to ensure we test the current run
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run the script
    result = subprocess.run([script_path, domain_path, generic_path, target_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStderr: {result.stderr}"

    assert os.path.exists(output_path), f"Output file {output_path} was not created."

    with open(output_path, 'r') as f:
        actual_lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    expected_lines = compute_expected_scores(domain_path, generic_path, target_path)

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output, got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines), 1):
        # We parse the actual output to allow minor formatting differences (like spaces instead of tabs if student messed up slightly, though tab is requested)
        actual_parts = actual.split()
        expected_parts = expected.split('\t')

        assert len(actual_parts) == 3, f"Line {i} does not have exactly 3 columns: '{actual}'"

        assert actual_parts[0] == expected_parts[0], f"Line {i}: Expected line number {expected_parts[0]}, got {actual_parts[0]}"

        actual_score = float(actual_parts[1])
        expected_score = float(expected_parts[1])
        assert math.isclose(actual_score, expected_score, abs_tol=0.0002), f"Line {i}: Expected score {expected_score:.4f}, got {actual_score:.4f}"

        assert actual_parts[2] == expected_parts[2], f"Line {i}: Expected classification {expected_parts[2]}, got {actual_parts[2]}"