# test_final_state.py

import os
import json
import csv
import pytest

OUTPUT_JSON_PATH = "/home/user/graph_exporter/output.json"
MAPPING_CSV_PATH = "/home/user/data/authors_papers.csv"
EXPECTED_QUERY = "UNWIND $batch AS row MERGE (a:Author {id: row.author_id}) MERGE (p:Paper {id: row.paper_id}) MERGE (a)-[:WROTE]->(p)"

def test_output_json_exists():
    """Verify that the expected output JSON file has been created."""
    assert os.path.isfile(OUTPUT_JSON_PATH), f"The output file {OUTPUT_JSON_PATH} was not found. Did you run the Rust program?"

def test_output_json_structure_and_query():
    """Verify the JSON structure and the exact Cypher query string."""
    with open(OUTPUT_JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {OUTPUT_JSON_PATH} does not contain valid JSON.")

    assert "query" in data, "The JSON is missing the 'query' key."
    assert "parameters" in data, "The JSON is missing the 'parameters' key."
    assert data["query"] == EXPECTED_QUERY, f"The query string does not match the expected value.\nExpected: {EXPECTED_QUERY}\nActual: {data['query']}"
    assert "batch" in data["parameters"], "The 'parameters' object is missing the 'batch' key."

def test_output_json_batch_data():
    """Verify that the batch data matches the authors_papers.csv mapping exactly."""
    # Read the expected data from the CSV
    expected_batch = []
    assert os.path.isfile(MAPPING_CSV_PATH), f"The mapping file {MAPPING_CSV_PATH} is missing."

    with open(MAPPING_CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expected_batch.append({
                "author_id": int(row["author_id"]),
                "paper_id": int(row["paper_id"])
            })

    # Sort expected batch
    expected_batch.sort(key=lambda x: (x["author_id"], x["paper_id"]))

    # Read the actual data from the JSON
    with open(OUTPUT_JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Invalid JSON in output file.")

    actual_batch = data.get("parameters", {}).get("batch", [])
    assert isinstance(actual_batch, list), "The 'batch' value should be a list."

    # Ensure all items have integer IDs
    for item in actual_batch:
        assert isinstance(item.get("author_id"), int), "author_id in batch must be an integer."
        assert isinstance(item.get("paper_id"), int), "paper_id in batch must be an integer."

    # Sort actual batch just in case, though the instructions said to sort it
    actual_batch_sorted = sorted(actual_batch, key=lambda x: (x.get("author_id", 0), x.get("paper_id", 0)))

    assert actual_batch_sorted == expected_batch, "The batch parameters do not match the expected relationships from the CSV."
    assert actual_batch == actual_batch_sorted, "The batch array in the JSON is not sorted by author_id ascending, then paper_id ascending."