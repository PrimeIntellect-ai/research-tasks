# test_final_state.py

import os
import csv
import math
import re
from collections import Counter
import pytest

def get_golden_pairs():
    """
    Recomputes the TF-IDF matrix and cosine similarities in pure Python
    to match scikit-learn's TfidfVectorizer with default settings.
    """
    data_path = '/home/user/data.csv'
    if not os.path.exists(data_path):
        pytest.fail(f"Missing data file: {data_path}")

    docs = []
    with open(data_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            docs.append((int(row['doc_id']), row['text']))

    tokenized_docs = []
    vocab = set()
    for doc_id, text in docs:
        # scikit-learn default token pattern
        tokens = re.findall(r"(?u)\b\w\w+\b", text.lower())
        tokenized_docs.append((doc_id, tokens))
        vocab.update(tokens)

    vocab = sorted(list(vocab))

    # Calculate Document Frequency (DF)
    df = Counter()
    for doc_id, tokens in tokenized_docs:
        df.update(set(tokens))

    n_docs = len(docs)
    idf = {}
    for term in vocab:
        # scikit-learn smooth_idf=True formula
        idf[term] = math.log((1 + n_docs) / (1 + df[term])) + 1.0

    # Calculate TF-IDF vectors
    tfidf_matrix = []
    for doc_id, tokens in tokenized_docs:
        tf = Counter(tokens)
        vec = []
        for term in vocab:
            vec.append(tf[term] * idf[term])
        # L2 normalization
        norm = math.sqrt(sum(v*v for v in vec))
        if norm > 0:
            vec = [v/norm for v in vec]
        tfidf_matrix.append((doc_id, vec))

    # Compute Cosine Similarity
    pairs = []
    for i in range(len(tfidf_matrix)):
        id1, vec1 = tfidf_matrix[i]
        for j in range(i+1, len(tfidf_matrix)):
            id2, vec2 = tfidf_matrix[j]
            sim = sum(v1*v2 for v1, v2 in zip(vec1, vec2))
            # Account for floating point inaccuracies
            if sim >= 0.8499999999:
                pairs.append(tuple(sorted([id1, id2])))

    return sorted(list(set(pairs)))


def test_benchmark_time():
    """Verify benchmark_time.txt exists and contains a valid float > 0."""
    path = "/home/user/benchmark_time.txt"
    assert os.path.exists(path), f"File not found: {path}"

    with open(path, "r", encoding='utf-8') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {path} is not a valid float: '{content}'")

    assert val > 0, f"Benchmark time must be greater than 0, got {val}"


def test_duplicates_csv():
    """Verify duplicates.csv contains the exact correct pairs, sorted properly."""
    path = "/home/user/duplicates.csv"
    assert os.path.exists(path), f"File not found: {path}"

    golden_pairs = get_golden_pairs()

    actual_pairs = []
    with open(path, "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"{path} is empty")

        assert headers == ['id1', 'id2'], f"Incorrect headers in {path}. Expected ['id1', 'id2'], got {headers}"

        for i, row in enumerate(reader, start=2):
            assert len(row) == 2, f"Row {i} does not have exactly 2 columns"
            try:
                id1, id2 = int(row[0]), int(row[1])
            except ValueError:
                pytest.fail(f"Row {i} contains non-integer IDs: {row}")

            assert id1 < id2, f"Row {i} violates id1 < id2 rule: {id1} >= {id2}"
            actual_pairs.append((id1, id2))

    # The file should be sorted by id1 ascending, then id2 ascending
    sorted_actual_pairs = sorted(actual_pairs)
    assert actual_pairs == sorted_actual_pairs, f"{path} is not correctly sorted by id1 then id2"

    # Check that the pairs match the expected ground truth exactly
    assert actual_pairs == golden_pairs, (
        f"Duplicate pairs mismatch.\n"
        f"Expected: {golden_pairs}\n"
        f"Actual:   {actual_pairs}"
    )