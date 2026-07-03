# test_final_state.py

import os
import re
import csv
import json
import subprocess
import pytest

def get_trigrams(text):
    return set(text[i:i+3] for i in range(len(text) - 2))

def jaccard(set1, set2):
    if not set1 and not set2:
        return 1.0
    return len(set1 & set2) / len(set1 | set2)

def reference_pipeline():
    raw_path = "/home/user/raw_reviews.txt"
    if not os.path.exists(raw_path):
        return []

    extracted = []
    with open(raw_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse format: ID:<id> | TEXT:<review_text> | META:<messy_metadata>
            parts = line.split(" | ")
            if len(parts) != 3:
                continue

            id_str = parts[0].replace("ID:", "").strip()
            text_str = parts[1].replace("TEXT:", "").strip()
            meta_str = parts[2].replace("META:", "").strip()

            # Extract rating
            rating_match = re.search(r'rating:(\d)|(\d) stars|score=(\d)', meta_str)
            if rating_match:
                rating = int(next(g for g in rating_match.groups() if g is not None))
                extracted.append((int(id_str), rating, text_str))

    # Stratified sampling
    sampled = []
    for r in range(1, 6):
        rating_records = [rec for rec in extracted if rec[1] == r]
        rating_records.sort(key=lambda x: x[0])
        sampled.extend(rating_records[:5])

    # Compute similarity
    similar_pairs = []
    for i in range(len(sampled)):
        for j in range(i + 1, len(sampled)):
            id1, _, text1 = sampled[i]
            id2, _, text2 = sampled[j]

            tri1 = get_trigrams(text1)
            tri2 = get_trigrams(text2)

            sim = jaccard(tri1, tri2)
            if sim >= 0.4:
                pair = [id1, id2] if id1 < id2 else [id2, id1]
                similar_pairs.append(pair)

    similar_pairs.sort(key=lambda x: (x[0], x[1]))
    return similar_pairs

def test_makefile_execution():
    # Ensure Makefile exists
    makefile_path = "/home/user/Makefile"
    assert os.path.exists(makefile_path), f"{makefile_path} does not exist."

    # Touch raw_reviews.txt to force make to run
    raw_path = "/home/user/raw_reviews.txt"
    os.utime(raw_path, None)

    # Run make
    result = subprocess.run(["make", "-C", "/home/user/"], capture_output=True, text=True)
    assert result.returncode == 0, f"make command failed with error:\n{result.stderr}"

def test_extracted_csv():
    extracted_path = "/home/user/extracted.csv"
    assert os.path.exists(extracted_path), f"{extracted_path} does not exist."

    with open(extracted_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["id", "rating", "text"], f"Incorrect header in extracted.csv: {header}"

        rows = list(reader)
        assert len(rows) > 0, "extracted.csv is empty."

def test_sampled_csv():
    sampled_path = "/home/user/sampled.csv"
    assert os.path.exists(sampled_path), f"{sampled_path} does not exist."

    with open(sampled_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["id", "rating", "text"], f"Incorrect header in sampled.csv: {header}"

        rows = list(reader)
        assert len(rows) == 25, f"sampled.csv should have exactly 25 records, found {len(rows)}."

def test_similar_pairs_json():
    json_path = "/home/user/similar_pairs.json"
    assert os.path.exists(json_path), f"{json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            student_pairs = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {json_path} as valid JSON.")

    expected_pairs = reference_pipeline()

    assert isinstance(student_pairs, list), "similar_pairs.json must contain a JSON array."

    # Ensure inner items are lists
    student_pairs = [list(p) for p in student_pairs]

    assert student_pairs == expected_pairs, (
        f"Similar pairs do not match expected output.\n"
        f"Expected: {expected_pairs}\n"
        f"Found: {student_pairs}"
    )

def test_multiprocessing_used():
    sim_script = "/home/user/similarity.py"
    assert os.path.exists(sim_script), f"{sim_script} does not exist."

    with open(sim_script, "r") as f:
        content = f.read()

    assert "multiprocessing" in content or "Pool" in content or "Process" in content, \
        "The similarity.py script does not appear to use the multiprocessing module."