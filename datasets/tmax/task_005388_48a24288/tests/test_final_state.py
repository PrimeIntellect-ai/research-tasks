# test_final_state.py

import os
import sqlite3
import csv
import subprocess
import pytest

def test_sql_and_csv_output():
    csv_path = "/home/user/projected_graph.csv"
    assert os.path.exists(csv_path), f"Missing CSV output at {csv_path}"

    db_path = "/app/research.db"
    assert os.path.exists(db_path), f"Missing database at {db_path}"

    # Recompute the expected result
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Force full table scan or just rely on correct filtering in python
    # We will do it in python to be absolutely sure we get the truth
    cursor.execute("SELECT source_id, target_id FROM edges WHERE is_deleted = 0")
    edges = cursor.fetchall()

    cursor.execute("SELECT id, title, year, citations FROM papers WHERE is_deleted = 0")
    papers = {row[0]: {'title': row[1], 'year': row[2], 'citations': row[3]} for row in cursor.fetchall()}

    adj = {}
    for src, tgt in edges:
        if src not in adj:
            adj[src] = []
        adj[src].append(tgt)

    start_node = 4582
    max_depth = 3

    visited = set()
    queue = [(start_node, 0)]

    while queue:
        node, depth = queue.pop(0)
        if node not in visited:
            visited.add(node)
            if depth < max_depth:
                for neighbor in adj.get(node, []):
                    queue.append((neighbor, depth + 1))

    # Now get papers and rank them
    subgraph_papers = []
    for node in visited:
        if node in papers:
            subgraph_papers.append((node, papers[node]['title'], papers[node]['year'], papers[node]['citations']))

    # Group by year and rank
    by_year = {}
    for p in subgraph_papers:
        y = p[2]
        if y not in by_year:
            by_year[y] = []
        by_year[y].append(p)

    ranked_papers = []
    for y, items in by_year.items():
        # sort by citations DESC
        items.sort(key=lambda x: x[3], reverse=True)
        # assign rank
        for i, item in enumerate(items):
            ranked_papers.append((item[0], item[1], item[2], item[3], i + 1))

    # sort by year ASC, rank ASC
    ranked_papers.sort(key=lambda x: (x[2], x[4]))

    expected_top_50 = ranked_papers[:50]

    # Read CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = list(reader)

    assert len(rows) == len(expected_top_50), f"Expected {len(expected_top_50)} rows in CSV, got {len(rows)}"

    for i, (actual, expected) in enumerate(zip(rows, expected_top_50)):
        # Just check ID to be robust against header/column ordering variations if possible,
        # but the task implies standard projection. Assuming ID is first or present.
        actual_str = ",".join(actual)
        assert str(expected[0]) in actual_str, f"Row {i+1} mismatch: expected paper ID {expected[0]} in {actual}"

def test_path_filter_executable():
    bin_path = "/home/user/path_filter"
    assert os.path.exists(bin_path), f"Missing executable at {bin_path}"
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable"

def test_adversarial_corpus_clean():
    bin_path = "/home/user/path_filter"
    clean_dir = "/app/corpus/clean"

    if not os.path.exists(clean_dir):
        pytest.skip(f"Clean corpus dir {clean_dir} not found")

    failed_files = []
    total_files = 0

    for fname in os.listdir(clean_dir):
        total_files += 1
        fpath = os.path.join(clean_dir, fname)
        with open(fpath, 'rb') as f:
            input_data = f.read()

        proc = subprocess.run([bin_path], input=input_data, capture_output=True)

        if proc.returncode != 0 or proc.stdout != input_data:
            failed_files.append(fname)

    assert not failed_files, f"{len(failed_files)} of {total_files} clean modified/rejected: {failed_files[:5]}"

def test_adversarial_corpus_evil():
    bin_path = "/home/user/path_filter"
    evil_dir = "/app/corpus/evil"

    if not os.path.exists(evil_dir):
        pytest.skip(f"Evil corpus dir {evil_dir} not found")

    failed_files = []
    total_files = 0

    for fname in os.listdir(evil_dir):
        total_files += 1
        fpath = os.path.join(evil_dir, fname)
        with open(fpath, 'rb') as f:
            input_data = f.read()

        proc = subprocess.run([bin_path], input=input_data, capture_output=True)

        # Evil files should output nothing or only the clean lines if mixed.
        # The prompt implies each file might be a single line or multiple.
        # Assuming evil paths must be completely rejected (omitted from stdout).
        # We will check if the stdout is empty, assuming evil files only contain evil lines.
        if proc.returncode != 0 or proc.stdout.strip():
            failed_files.append(fname)

    assert not failed_files, f"{len(failed_files)} of {total_files} evil bypassed: {failed_files[:5]}"