# test_final_state.py

import os
import math
import re
import csv
import pytest

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    return [t for t in text.split(' ') if t]

def bow(tokens):
    vec = {}
    for t in tokens:
        vec[t] = vec.get(t, 0) + 1
    return vec

def dot(v1, v2):
    return sum(v1.get(k, 0) * v2.get(k, 0) for k in v1)

def norm(v):
    return math.sqrt(sum(val**2 for val in v.values()))

def cosine(v1, v2):
    n1 = norm(v1)
    n2 = norm(v2)
    if n1 == 0 or n2 == 0: return 0.0
    return dot(v1, v2) / (n1 * n2)

def compute_expected_results():
    corpus_path = "/home/user/corpus.txt"
    queries_path = "/home/user/queries.txt"

    with open(corpus_path, 'r') as f:
        corpus = [bow(tokenize(line)) for line in f]

    with open(queries_path, 'r') as f:
        queries = [bow(tokenize(line)) for line in f]

    top_scores = []
    results = []
    for q_idx, q in enumerate(queries):
        best_idx = -1
        best_score = -1.0
        for c_idx, c in enumerate(corpus):
            score = cosine(q, c)
            if score > best_score:
                best_score = score
                best_idx = c_idx
        top_scores.append(best_score)
        results.append((q_idx, best_idx, best_score))

    N = len(top_scores)
    mean = sum(top_scores) / N
    variance = sum((x - mean)**2 for x in top_scores) / (N - 1)
    std_dev = math.sqrt(variance)

    ci_margin = 1.96 * (std_dev / math.sqrt(N))
    ci_lower = mean - ci_margin
    ci_upper = mean + ci_margin

    return results, mean, ci_lower, ci_upper

def test_summary_file_exists():
    summary_path = "/home/user/summary.csv"
    assert os.path.isfile(summary_path), f"Expected output file {summary_path} does not exist."

def test_summary_contents():
    summary_path = "/home/user/summary.csv"
    assert os.path.isfile(summary_path), f"Expected output file {summary_path} does not exist."

    expected_results, expected_mean, expected_ci_lower, expected_ci_upper = compute_expected_results()

    with open(summary_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == len(expected_results) + 3, "Incorrect number of lines in summary.csv"

    assert lines[0] == "QueryIndex,TopCorpusIndex,CosineSimilarity", "Header for results is incorrect."

    for i in range(len(expected_results)):
        parts = lines[i+1].split(',')
        assert len(parts) == 3, f"Line {i+1} does not have 3 columns."
        q_idx, c_idx, score = expected_results[i]

        assert int(parts[0]) == q_idx, f"Expected QueryIndex {q_idx}, got {parts[0]}"
        assert int(parts[1]) == c_idx, f"Expected TopCorpusIndex {c_idx}, got {parts[1]}"
        assert math.isclose(float(parts[2]), score, abs_tol=1e-3), f"Expected CosineSimilarity {score:.4f}, got {parts[2]}"

    assert lines[-2] == "Mean,CI_Lower,CI_Upper", "Header for statistics is incorrect."

    stat_parts = lines[-1].split(',')
    assert len(stat_parts) == 3, "Statistics line does not have 3 columns."

    assert math.isclose(float(stat_parts[0]), expected_mean, abs_tol=1e-3), f"Expected Mean {expected_mean:.4f}, got {stat_parts[0]}"
    assert math.isclose(float(stat_parts[1]), expected_ci_lower, abs_tol=1e-3), f"Expected CI_Lower {expected_ci_lower:.4f}, got {stat_parts[1]}"
    assert math.isclose(float(stat_parts[2]), expected_ci_upper, abs_tol=1e-3), f"Expected CI_Upper {expected_ci_upper:.4f}, got {stat_parts[2]}"