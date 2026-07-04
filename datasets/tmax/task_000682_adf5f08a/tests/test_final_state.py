# test_final_state.py

import os
import struct
import math
import pytest

def compute_expected_top5():
    query_path = "/home/user/query.bin"
    embeddings_path = "/home/user/embeddings.bin"

    if not os.path.exists(query_path) or not os.path.exists(embeddings_path):
        return []

    with open(query_path, 'rb') as f:
        q_data = f.read()
    if len(q_data) != 128 * 4:
        return []
    query = struct.unpack('128f', q_data)

    with open(embeddings_path, 'rb') as f:
        e_data = f.read()

    num_embeddings = len(e_data) // (128 * 4)
    sims = []

    norm_q = math.sqrt(sum(q * q for q in query))

    for i in range(num_embeddings):
        emb = struct.unpack('128f', e_data[i * 128 * 4 : (i + 1) * 128 * 4])
        dot = sum(q * e for q, e in zip(query, emb))
        norm_e = math.sqrt(sum(e * e for e in emb))

        sim = dot / (norm_q * norm_e) if norm_q * norm_e != 0 else 0
        sims.append((i, sim))

    sims.sort(key=lambda x: x[1], reverse=True)
    return [str(x[0]) for x in sims[:5]]

def test_sim_search_c_fixed():
    path = "/home/user/sim_search.c"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "int dot = 0;" not in content, "The bug 'int dot = 0;' is still present in sim_search.c"
    assert "float dot" in content or "double dot" in content, "The dot product variable should be declared as a float or double."

def test_sim_search_executable_exists():
    path = "/home/user/sim_search"
    assert os.path.isfile(path), f"Executable missing: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_top5_txt_correct():
    path = "/home/user/top5.txt"
    assert os.path.isfile(path), f"File missing: {path}"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_top5 = compute_expected_top5()
    assert expected_top5, "Could not compute expected top 5 (missing or invalid binary files)."

    assert len(lines) == 5, f"Expected exactly 5 lines in top5.txt, got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_top5)):
        assert actual == expected, f"Mismatch at rank {i+1}: expected {expected}, got {actual}"