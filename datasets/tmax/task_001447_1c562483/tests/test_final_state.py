# test_final_state.py

import os
import glob
import subprocess
import sqlite3
import shutil
import pytest

def test_step1_video_extraction():
    frames_dir = "/home/user/frames"
    count_file = "/home/user/frame_count.txt"

    assert os.path.isdir(frames_dir), f"Frames directory does not exist at {frames_dir}."
    assert os.path.isfile(count_file), f"Frame count file does not exist at {count_file}."

    # Check that there are JPEGs in the directory
    jpegs = glob.glob(os.path.join(frames_dir, "*.jpg")) + glob.glob(os.path.join(frames_dir, "*.jpeg"))
    assert len(jpegs) > 0, "No JPEG frames found in the frames directory."

    with open(count_file, "r") as f:
        count_str = f.read().strip()

    assert count_str.isdigit(), "Frame count file does not contain a valid integer."

    expected_count = len(jpegs)
    actual_count = int(count_str)
    assert actual_count == expected_count, f"Frame count in file ({actual_count}) does not match the actual number of extracted JPEG frames ({expected_count})."

def test_step2_database_indexes():
    sql_file = "/home/user/indexes.sql"
    assert os.path.isfile(sql_file), f"SQL file does not exist at {sql_file}."

    with open(sql_file, "r") as f:
        sql_script = f.read()

    db_path = "/app/metrics.db"
    test_db = "/tmp/test_metrics.db"
    shutil.copy2(db_path, test_db)

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    try:
        cursor.executescript(sql_script)
    except Exception as e:
        conn.close()
        pytest.fail(f"Failed to execute indexes.sql: {e}")

    query = """
    EXPLAIN QUERY PLAN
    SELECT n.region, SUM(t.bytes_transferred)
    FROM nodes n
    JOIN traffic_logs t ON n.id = t.source_node_id
    WHERE t.timestamp >= '2024-01-01' AND t.timestamp < '2024-02-01'
    GROUP BY n.region;
    """
    cursor.execute(query)
    plan = cursor.fetchall()
    conn.close()

    plan_str = " ".join([row[-1] for row in plan]).upper()

    # We expect an index to be used to optimize the query
    assert "INDEX" in plan_str, "No index was used in the query plan after applying indexes.sql. The query is not optimized."

def test_step3_adversarial_corpus():
    script_path = "/home/user/validate_graphs.py"
    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    evil_in = "/app/corpora/evil"
    clean_in = "/app/corpora/clean"
    evil_out = "/tmp/test_evil"
    clean_out = "/tmp/test_clean"

    os.makedirs(evil_out, exist_ok=True)
    os.makedirs(clean_out, exist_ok=True)

    # Run script on evil corpus
    res_evil = subprocess.run(["python3", script_path, evil_in, evil_out], capture_output=True, text=True)
    assert res_evil.returncode == 0, f"Script failed on evil corpus with exit code {res_evil.returncode}:\n{res_evil.stderr}"

    # Run script on clean corpus
    res_clean = subprocess.run(["python3", script_path, clean_in, clean_out], capture_output=True, text=True)
    assert res_clean.returncode == 0, f"Script failed on clean corpus with exit code {res_clean.returncode}:\n{res_clean.stderr}"

    evil_input_files = set([f for f in os.listdir(evil_in) if f.endswith('.json')])
    clean_input_files = set([f for f in os.listdir(clean_in) if f.endswith('.json')])

    evil_output_files = set(os.listdir(evil_out))
    clean_output_files = set(os.listdir(clean_out))

    # Assert evil corpus is rejected completely
    evil_bypassed = evil_output_files.intersection(evil_input_files)
    assert len(evil_bypassed) == 0, f"{len(evil_bypassed)} of {len(evil_input_files)} evil bypassed: {', '.join(list(evil_bypassed)[:5])}"

    # Assert clean corpus is preserved completely
    clean_missing = clean_input_files - clean_output_files
    assert len(clean_missing) == 0, f"{len(clean_missing)} of {len(clean_input_files)} clean modified or rejected: {', '.join(list(clean_missing)[:5])}"