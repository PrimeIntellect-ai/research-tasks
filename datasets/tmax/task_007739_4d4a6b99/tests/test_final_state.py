# test_final_state.py

import os
import math

def test_c_source_exists():
    path = "/home/user/etl_recommender.c"
    assert os.path.isfile(path), f"C source file {path} is missing."

def test_executable_exists():
    path = "/home/user/etl_recommender"
    assert os.path.isfile(path), f"Executable {path} is missing. Did you compile the code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_recommendations_csv_exists_and_content():
    path = "/home/user/recommendations.csv"
    assert os.path.isfile(path), f"Output file {path} is missing. Did you run the executable?"

    # Recompute the expected results based on the initial data
    users = [
        (1, 0.0, 0.0),
        (2, 3.0, 4.0),
        (3, -1.0, -1.0)
    ]
    items = [
        (101, 1.0, 1.0),
        (102, 0.0, 5.0),
        (103, -2.0, -2.0)
    ]

    expected_lines = []
    for u_id, ux, uy in users:
        min_dist = float('inf')
        best_item = -1
        for i_id, ix, iy in items:
            dist = math.sqrt((ux - ix)**2 + (uy - iy)**2)
            # Tie breaking: pick smaller item_id
            if dist < min_dist - 1e-9:
                min_dist = dist
                best_item = i_id
            elif abs(dist - min_dist) <= 1e-9:
                if i_id < best_item:
                    best_item = i_id

        expected_lines.append(f"{u_id},{best_item},{min_dist:.4f}")

    expected_content = "\n".join(expected_lines)

    with open(path, "r") as f:
        content = f.read().strip()

    # Normalize line endings
    actual_content = "\n".join(line.strip() for line in content.splitlines() if line.strip())

    assert actual_content == expected_content, (
        f"Content of {path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )