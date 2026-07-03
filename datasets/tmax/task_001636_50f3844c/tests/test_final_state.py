# test_final_state.py

import os
import json
import csv
import math
import pytest

def test_rust_project_exists():
    """Verify that the Rust project was created in the correct directory."""
    cargo_toml_path = "/home/user/retrieval_tool/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), (
        f"Expected a Rust project with a Cargo.toml at {cargo_toml_path}, but it was not found."
    )

def test_top_matches_output():
    """Verify the JSON output file exists, is correctly formatted, and contains the correct results."""
    json_path = "/home/user/top_matches.json"
    assert os.path.isfile(json_path), f"Expected output file {json_path} does not exist."

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON root must be an array."
    assert len(data) == 3, f"Expected exactly 3 top matches, but got {len(data)}."

    csv_path = "/home/user/embeddings.csv"
    assert os.path.isfile(csv_path), f"Input file {csv_path} is missing."

    query = [0.12, 0.88, 0.34, 0.71, 0.55]
    mag_q = math.sqrt(sum(x * x for x in query))

    results = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_id = int(row["id"])
            vec = [
                float(row["v1"]),
                float(row["v2"]),
                float(row["v3"]),
                float(row["v4"]),
                float(row["v5"]),
            ]
            dot = sum(q * v for q, v in zip(query, vec))
            mag_v = math.sqrt(sum(v * v for v in vec))
            if mag_v == 0:
                sim = 0.0
            else:
                sim = dot / (mag_q * mag_v)
            results.append((sim, row_id))

    # Sort primarily by similarity descending, then by id ascending (lower id wins ties)
    results.sort(key=lambda x: (-x[0], x[1]))
    top_3 = results[:3]

    for i in range(3):
        expected_sim, expected_id = top_3[i]
        expected_sim_rounded = round(expected_sim, 6)

        item = data[i]
        assert "id" in item, f"Object at index {i} is missing the 'id' key."
        assert "similarity" in item, f"Object at index {i} is missing the 'similarity' key."

        actual_id = item["id"]
        actual_sim = item["similarity"]

        assert actual_id == expected_id, (
            f"Rank {i+1} mismatch: expected ID {expected_id}, but got {actual_id}."
        )
        assert math.isclose(actual_sim, expected_sim_rounded, abs_tol=1e-5), (
            f"Rank {i+1} (ID {expected_id}) similarity mismatch: "
            f"expected {expected_sim_rounded}, but got {actual_sim}."
        )