# test_final_state.py

import os
import json
import math
import urllib.request
import urllib.error
import re
import sqlite3
import pytest

def compute_expected_similarities():
    raw_data_path = '/home/user/raw_data.jsonl'
    if not os.path.exists(raw_data_path):
        pytest.fail(f"Raw data file {raw_data_path} is missing.")

    docs = {}
    with open(raw_data_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            docs[item['id']] = item['text']

    # Tokenize
    tokenized_docs = {}
    for doc_id, text in docs.items():
        # Lowercase, remove non-alphanumeric/spaces
        cleaned = re.sub(r'[^a-z0-9\s]', '', text.lower())
        tokens = [t for t in cleaned.split(' ') if t]
        tokenized_docs[doc_id] = tokens

    N = len(tokenized_docs)

    # Compute DF
    df = {}
    for doc_id, tokens in tokenized_docs.items():
        unique_tokens = set(tokens)
        for t in unique_tokens:
            df[t] = df.get(t, 0) + 1

    # Compute TF-IDF
    tf_idf = {}
    for doc_id, tokens in tokenized_docs.items():
        tf_idf[doc_id] = {}
        tf = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
        for t, count in tf.items():
            idf = math.log(N / df[t])
            tf_idf[doc_id][t] = count * idf

    # Compute norms
    norms = {}
    for doc_id, vector in tf_idf.items():
        norms[doc_id] = math.sqrt(sum(v**2 for v in vector.values()))

    def get_top_3(target_id):
        target_vec = tf_idf[target_id]
        target_norm = norms[target_id]

        similarities = []
        for doc_id, vector in tf_idf.items():
            if doc_id == target_id:
                continue
            dot_product = sum(target_vec.get(t, 0) * vector.get(t, 0) for t in set(target_vec) & set(vector))
            if target_norm == 0 or norms[doc_id] == 0:
                sim = 0
            else:
                sim = dot_product / (target_norm * norms[doc_id])
            similarities.append((doc_id, sim))

        # Sort by similarity descending, then doc_id ascending
        similarities.sort(key=lambda x: (-x[1], x[0]))
        return [x[0] for x in similarities[:3]]

    return get_top_3

def test_database_exists():
    db_path = '/home/user/etl_store.db'
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."
    assert os.path.isfile(db_path), f"{db_path} is not a file."

    # Check if it's a valid sqlite database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        assert len(tables) > 0, "Database exists but contains no tables."
    except sqlite3.Error as e:
        pytest.fail(f"Failed to read SQLite database at {db_path}: {e}")

def test_server_running_and_correct():
    get_top_3 = compute_expected_similarities()
    expected_doc3 = get_top_3("doc3")

    url = "http://127.0.0.1:8080/similar?id=doc3"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert "similar_ids" in data, "Response JSON missing 'similar_ids' key."
            assert data["similar_ids"] == expected_doc3, f"Expected {expected_doc3} for doc3, got {data['similar_ids']}"
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to server at {url}: {e}")
    except json.JSONDecodeError:
        pytest.fail("Server response is not valid JSON.")

def test_doc1_recommendations_file():
    output_path = '/home/user/doc1_recommendations.json'
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    get_top_3 = compute_expected_similarities()
    expected_doc1 = get_top_3("doc1")

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} does not contain valid JSON.")

    assert "similar_ids" in data, f"JSON in {output_path} missing 'similar_ids' key."
    assert data["similar_ids"] == expected_doc1, f"Expected {expected_doc1} in {output_path}, got {data['similar_ids']}"