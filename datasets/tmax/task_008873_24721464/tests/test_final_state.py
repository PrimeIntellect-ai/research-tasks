# test_final_state.py

import os
import csv
import json
import math
import struct
import re
import pytest

def read_npy(filepath):
    """Minimal pure-Python NPY file reader for 1D/2D float32 arrays."""
    with open(filepath, 'rb') as f:
        magic = f.read(6)
        if magic != b'\x93NUMPY':
            raise ValueError(f"Not a valid .npy file: {filepath}")
        major, minor = struct.unpack('<BB', f.read(2))
        if major == 1:
            header_len = struct.unpack('<H', f.read(2))[0]
        else:
            header_len = struct.unpack('<I', f.read(4))[0]
        header_str = f.read(header_len).decode('ascii')

        # Safely evaluate the header dict
        header_dict = eval(header_str.strip())
        shape = header_dict['shape']
        descr = header_dict['descr']

        if descr != '<f4':
            raise ValueError(f"Unsupported dtype: {descr}")

        data = f.read()
        num_elements = 1
        for dim in shape:
            num_elements *= dim

        values = struct.unpack('<' + 'f' * num_elements, data)

        if len(shape) == 1:
            return list(values)
        elif len(shape) == 2:
            res = []
            for i in range(shape[0]):
                res.append(list(values[i*shape[1]:(i+1)*shape[1]]))
            return res
        else:
            raise ValueError("Only 1D and 2D arrays are supported")

def compute_ground_truth():
    """Derive the expected output directly from the data and model files."""
    # Read vocab
    with open("/home/user/model/vocab.json", "r") as f:
        vocab = json.load(f)

    # Read weights
    embeddings = read_npy("/home/user/model/embeddings.npy")
    linear_w = read_npy("/home/user/model/linear_w.npy")
    linear_b = read_npy("/home/user/model/linear_b.npy")

    # Read reviews
    reviews = []
    with open("/home/user/data/reviews.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            reviews.append(row)

    # Process reviews
    review_embeddings = {}
    for review in reviews:
        text = review["text"].lower()
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        tokens = text.split()

        # Map to indices
        indices = [vocab.get(token, 0) for token in tokens]

        # Mean pooling
        if not indices:
            pooled = [0.0] * 32
        else:
            pooled = [0.0] * 32
            for idx in indices:
                emb = embeddings[idx]
                for i in range(32):
                    pooled[i] += emb[i]
            for i in range(32):
                pooled[i] /= len(indices)

        # Linear layer
        proj = [0.0] * 16
        for i in range(16):
            val = 0.0
            for j in range(32):
                val += linear_w[i][j] * pooled[j]
            proj[i] = val + linear_b[i]

        review_embeddings[review["id"]] = proj

    # Compute similarities
    ids = list(review_embeddings.keys())
    pairs = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            id1, id2 = ids[i], ids[j]
            if id1 > id2:
                id1, id2 = id2, id1

            vec1 = review_embeddings[id1]
            vec2 = review_embeddings[id2]

            dot = sum(vec1[k] * vec2[k] for k in range(16))
            norm1 = math.sqrt(sum(vec1[k]**2 for k in range(16)))
            norm2 = math.sqrt(sum(vec2[k]**2 for k in range(16)))

            if norm1 == 0 or norm2 == 0:
                sim = 0.0
            else:
                sim = dot / (norm1 * norm2)

            pairs.append((id1, id2, round(sim, 4)))

    # Sort pairs: similarity descending, then id1 asc, then id2 asc
    pairs.sort(key=lambda x: (-x[2], x[0], x[1]))
    return pairs[:3]

def test_run_pipeline_script_exists():
    """Test that the run_pipeline.sh script exists."""
    assert os.path.isfile("/home/user/run_pipeline.sh"), "The script /home/user/run_pipeline.sh is missing."

def test_output_file_exists():
    """Test that the output CSV file was created."""
    assert os.path.isfile("/home/user/output/top_pairs.csv"), "The output file /home/user/output/top_pairs.csv is missing."

def test_output_file_content():
    """Test that the output CSV file contains the correct top 3 pairs."""
    output_path = "/home/user/output/top_pairs.csv"

    with open(output_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["id1", "id2", "similarity"], f"Incorrect CSV header. Expected ['id1', 'id2', 'similarity'], got {header}"

        rows = list(reader)

    assert len(rows) == 3, f"Expected exactly 3 rows of data, got {len(rows)}."

    expected_pairs = compute_ground_truth()

    for i, (row, expected) in enumerate(zip(rows, expected_pairs)):
        assert len(row) == 3, f"Row {i+1} does not have 3 columns."
        id1, id2, sim_str = row

        assert id1 == expected[0], f"Row {i+1} id1 mismatch: expected {expected[0]}, got {id1}"
        assert id2 == expected[1], f"Row {i+1} id2 mismatch: expected {expected[1]}, got {id2}"

        try:
            sim = float(sim_str)
        except ValueError:
            pytest.fail(f"Row {i+1} similarity is not a valid float: {sim_str}")

        assert math.isclose(sim, expected[2], abs_tol=1e-4), f"Row {i+1} similarity mismatch: expected {expected[2]}, got {sim}"