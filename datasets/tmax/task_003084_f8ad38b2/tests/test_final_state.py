# test_final_state.py

import os
import json
import sqlite3
import time
import subprocess
import pytest

def get_expected_distances(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        WITH RECURSIVE author_paths(id, distance) AS (
            SELECT 1, 0
            UNION ALL
            SELECT coauthors.author2, author_paths.distance + 1
            FROM author_paths
            JOIN coauthors ON author_paths.id = coauthors.author1
            WHERE author_paths.distance < 20
        )
        SELECT id, MIN(distance) FROM author_paths GROUP BY id;
    """)
    expected = {str(r[0]): r[1] for r in c.fetchall()}
    conn.close()
    return expected

def test_script_execution_and_accuracy():
    script_path = '/home/user/generate_report.py'
    db_path = '/home/user/dataset/collaborations.db'
    output_path = '/home/user/distances.json'

    # Ensure script exists
    assert os.path.isfile(script_path), f"Script {script_path} not found."

    # Remove previous output if exists
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run the script and measure time
    start_time = time.time()
    try:
        subprocess.run(["python3", script_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed with error: {e.stderr}")

    elapsed = time.time() - start_time

    # Metric threshold check
    assert elapsed <= 1.0, f"Execution time {elapsed:.3f}s exceeded the 1.0s threshold."

    # Check output file exists
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    # Load actual output
    with open(output_path, 'r') as f:
        try:
            actual_distances = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} does not contain valid JSON.")

    # Calculate expected output
    expected_distances = get_expected_distances(db_path)

    # Compare
    assert actual_distances == expected_distances, "The computed shortest paths in distances.json do not match the true shortest paths."