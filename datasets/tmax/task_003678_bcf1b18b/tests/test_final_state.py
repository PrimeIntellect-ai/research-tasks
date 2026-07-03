# test_final_state.py

import os
import subprocess
import sqlite3
import csv
import tempfile
import pytest

def test_video_frame_extraction():
    output_csv = "/home/user/keyframes.csv"
    assert os.path.isfile(output_csv), f"Missing keyframes CSV file at {output_csv}"

    # Generate ground truth
    video_path = "/app/foraging_behavior.mp4"
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "frame=pkt_pts_time,pict_type",
        "-of", "csv=print_section=0", video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    expected_timestamps = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split(',')
        if len(parts) >= 2 and parts[1] == 'I':
            expected_timestamps.append(float(parts[0]))

    expected_timestamps.sort()

    # Read student CSV
    student_timestamps = []
    with open(output_csv, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['timestamp'], "CSV header must be exactly 'timestamp'"
        for row in reader:
            if row:
                student_timestamps.append(float(row[0]))

    assert student_timestamps == expected_timestamps, "Extracted keyframe timestamps do not match the expected I-frame timestamps"

def test_adversarial_metadata_filtering():
    script_path = "/home/user/cycle_detector.py"
    assert os.path.isfile(script_path), f"Missing script at {script_path}"

    clean_dir = "/app/taxonomy_corpus/clean"
    evil_dir = "/app/taxonomy_corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    failed_clean = []
    for cf in clean_files:
        res = subprocess.run(["python3", script_path, cf], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        res = subprocess.run(["python3", script_path, ef], capture_output=True)
        if res.returncode == 0:
            failed_evil.append(os.path.basename(ef))

    error_msg = []
    if failed_evil:
        error_msg.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        error_msg.append(f"{len(failed_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(failed_clean)}")

    assert not error_msg, "; ".join(error_msg)

def test_database_schema_and_index():
    schema_path = "/home/user/schema.sql"
    assert os.path.isfile(schema_path), f"Missing schema script at {schema_path}"

    with tempfile.NamedTemporaryFile(suffix=".db") as tmpdb:
        conn = sqlite3.connect(tmpdb.name)
        cursor = conn.cursor()

        with open(schema_path, 'r') as f:
            cursor.executescript(f.read())

        # Verify taxonomy table
        cursor.execute("PRAGMA table_info(taxonomy)")
        tax_cols = {row[1] for row in cursor.fetchall()}
        assert {'id', 'parent_id', 'name'}.issubset(tax_cols), "taxonomy table missing required columns"

        # Verify keyframes table
        cursor.execute("PRAGMA table_info(keyframes)")
        kf_cols = {row[1] for row in cursor.fetchall()}
        assert {'id', 'video_name', 'timestamp'}.issubset(kf_cols), "keyframes table missing required columns"

        # Verify index
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND name='idx_keyframes_video_time'")
        idx_row = cursor.fetchone()
        assert idx_row is not None, "Index idx_keyframes_video_time does not exist"
        idx_sql = idx_row[0].lower()
        assert "video_name" in idx_sql and "timestamp" in idx_sql, "Index does not cover video_name and timestamp"

        conn.close()

def test_recursive_query_construction():
    schema_path = "/home/user/schema.sql"
    query_path = "/home/user/recursive_export.sql"

    assert os.path.isfile(query_path), f"Missing recursive query script at {query_path}"

    with tempfile.NamedTemporaryFile(suffix=".db") as tmpdb:
        conn = sqlite3.connect(tmpdb.name)
        cursor = conn.cursor()

        with open(schema_path, 'r') as f:
            cursor.executescript(f.read())

        # Insert test data
        test_data = [
            (1, None, 'Animalia'),
            (2, 1, 'Chordata'),
            (3, 2, 'Mammalia'),
            (4, 3, 'Carnivora'),
            (5, None, 'Plantae')
        ]
        cursor.executemany("INSERT INTO taxonomy (id, parent_id, name) VALUES (?, ?, ?)", test_data)
        conn.commit()

        with open(query_path, 'r') as f:
            query = f.read()

        cursor.execute(query)
        results = cursor.fetchall()

        expected_results = [
            (1, 'Animalia', 'Animalia'),
            (2, 'Chordata', 'Animalia > Chordata'),
            (3, 'Mammalia', 'Animalia > Chordata > Mammalia'),
            (4, 'Carnivora', 'Animalia > Chordata > Mammalia > Carnivora'),
            (5, 'Plantae', 'Plantae')
        ]

        # Sort both just in case, though requirement says sorted by id ascending
        results_sorted = sorted(results, key=lambda x: x[0])
        expected_sorted = sorted(expected_results, key=lambda x: x[0])

        assert results_sorted == expected_sorted, "Recursive query output does not match expected hierarchical paths"

        # Also check if it actually sorts by id ascending as requested
        assert [r[0] for r in results] == [r[0] for r in expected_sorted], "Results are not sorted by id ascending"

        conn.close()