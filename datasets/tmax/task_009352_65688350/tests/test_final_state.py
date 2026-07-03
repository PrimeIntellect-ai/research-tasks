# test_final_state.py
import os
import math
import pytest

def get_embedding(text):
    text = text.strip()
    length = len(text) / 100.0
    words = len(text.split()) / 20.0
    vowels = sum(1 for c in text.lower() if c in "aeiou") / 50.0
    consonants = sum(1 for c in text.lower() if c in "bcdfghjklmnpqrstvwxyz") / 50.0
    ascii_sum = sum(ord(c) for c in text) % 10 / 10.0
    return [round(length, 3), round(words, 3), round(vowels, 3), round(consonants, 3), round(ascii_sum, 3)]

def cosine_similarity(v1, v2):
    dot = sum(x * y for x, y in zip(v1, v2))
    mag1 = math.sqrt(sum(x * x for x in v1))
    mag2 = math.sqrt(sum(x * x for x in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)

def test_index_tsv():
    index_path = "/home/user/index.tsv"
    assert os.path.isfile(index_path), f"{index_path} does not exist."

    with open(index_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected 5 lines in {index_path}, got {len(lines)}."

    dataset_dir = "/home/user/datasets"
    expected_files = sorted(os.listdir(dataset_dir))

    for i, expected_file in enumerate(expected_files):
        parts = lines[i].split("\t")
        assert len(parts) == 2, f"Line {i+1} in {index_path} is not tab-separated correctly."
        filename, vector_str = parts
        assert filename == expected_file, f"Expected filename {expected_file} at line {i+1}, got {filename}. Check sorting."

        with open(os.path.join(dataset_dir, expected_file), "r") as df:
            content = df.read()

        expected_vec = get_embedding(content)
        expected_vec_str = ",".join(str(v) for v in expected_vec)

        assert vector_str == expected_vec_str, f"Expected vector {expected_vec_str} for {filename}, got {vector_str}."

def test_recommendations():
    rec_path = "/home/user/recommendations.txt"
    assert os.path.isfile(rec_path), f"{rec_path} does not exist."

    with open(rec_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {rec_path}, got {len(lines)}."

    # Compute the expected top 2
    query = "Genomic and RNA sequencing"
    query_vec = get_embedding(query)

    dataset_dir = "/home/user/datasets"
    similarities = []
    for ds in os.listdir(dataset_dir):
        if not ds.endswith(".txt"): continue
        with open(os.path.join(dataset_dir, ds), "r") as df:
            content = df.read()
        ds_vec = get_embedding(content)
        sim = cosine_similarity(query_vec, ds_vec)
        similarities.append((sim, ds))

    similarities.sort(key=lambda x: x[0], reverse=True)
    expected_top1 = similarities[0][1]
    expected_top2 = similarities[1][1]

    assert lines[0] == expected_top1, f"Expected top recommendation to be {expected_top1}, got {lines[0]}."
    assert lines[1] == expected_top2, f"Expected second recommendation to be {expected_top2}, got {lines[1]}."

def test_test_result():
    res_path = "/home/user/test_result.txt"
    assert os.path.isfile(res_path), f"{res_path} does not exist."

    with open(res_path, "r") as f:
        content = f.read().strip()

    assert content == "PASS", f"Expected 'PASS' in {res_path}, got '{content}'."