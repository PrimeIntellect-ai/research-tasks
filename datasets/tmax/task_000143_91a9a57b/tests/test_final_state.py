# test_final_state.py

import os
import csv
import math

def test_results_csv_exists_and_correct():
    results_path = "/home/user/results.csv"
    assert os.path.isfile(results_path), f"File {results_path} is missing. Did you run the compiled C program?"

    with open(results_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 4, f"Expected header and 3 data rows in {results_path}, found {len(rows)} rows."

    header = rows[0]
    assert header == ["QueryID", "ClosestReferenceID", "Distance"], f"Header in {results_path} is incorrect. Got {header}"

    data = rows[1:]
    assert len(data) == 3, f"Expected exactly 3 data rows, got {len(data)}"

    # Expected values derived from properly scaling only on the reference set (rows 1-7)
    # Ref min_f1=10, max_f1=30; min_f2=10, max_f2=30

    # Query 8: (5,5) -> scaled (-0.25, -0.25)
    # Closest to Ref 1 (10,10) -> scaled (0, 0)
    # Distance: sqrt((-0.25)^2 + (-0.25)^2) = sqrt(0.125) = 0.3536

    # Query 9: (40,40) -> scaled (1.5, 1.5)
    # Closest to Ref 3 (30,30) -> scaled (1.0, 1.0)
    # Distance: sqrt((0.5)^2 + (0.5)^2) = sqrt(0.5) = 0.7071

    # Query 10: (14,26) -> scaled (0.2, 0.8)
    # Closest to Ref 4 (15,25) -> scaled (0.25, 0.75)
    # Distance: sqrt((-0.05)^2 + (0.05)^2) = sqrt(0.005) = 0.0707

    expected_results = {
        "8": {"closest": "1", "dist": 0.3536},
        "9": {"closest": "3", "dist": 0.7071},
        "10": {"closest": "4", "dist": 0.0707},
    }

    for row in data:
        assert len(row) == 3, f"Row {row} does not have exactly 3 columns."
        q_id, closest_id, dist_str = row

        assert q_id in expected_results, f"Unexpected QueryID {q_id} in results."

        expected = expected_results[q_id]
        assert closest_id == expected["closest"], f"For QueryID {q_id}, expected ClosestReferenceID {expected['closest']}, got {closest_id}."

        dist_val = float(dist_str)
        assert math.isclose(dist_val, expected["dist"], abs_tol=0.0001), \
            f"For QueryID {q_id}, expected Distance {expected['dist']}, got {dist_val}. Data leakage might not be fully fixed."

def test_pipeline_c_fixed():
    file_path = "/home/user/pipeline.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    # The loop calculating min/max should no longer iterate up to TOTAL_ROWS
    # It should iterate up to NUM_REF (or 7)

    # We can check that the bug is fixed by ensuring there isn't a loop over TOTAL_ROWS
    # right after the min/max initialization.
    # A robust way is to check that "i < NUM_REF" or "i < 7" is used for the min/max loop.

    # Find the min/max initialization
    init_idx = content.find("float min_f1")
    assert init_idx != -1, "Could not find min/max initialization in pipeline.c"

    # The next for loop should be bounded by NUM_REF or 7
    loop_idx = content.find("for", init_idx)
    assert loop_idx != -1, "Could not find the min/max calculation loop in pipeline.c"

    loop_condition = content[loop_idx:content.find("{", loop_idx)]
    assert "TOTAL_ROWS" not in loop_condition, "The min/max calculation loop still iterates over TOTAL_ROWS, causing data leakage."
    assert "NUM_REF" in loop_condition or "7" in loop_condition, "The min/max calculation loop should iterate over NUM_REF."