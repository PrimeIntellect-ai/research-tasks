# test_final_state.py
import os
import json
import pytest
import re

ETL_DIR = "/home/user/etl"
RAW_JSON_PATH = os.path.join(ETL_DIR, "raw_graph_results.json")
PROCESS_GO_PATH = os.path.join(ETL_DIR, "process.go")
PAGE_3_JSON_PATH = os.path.join(ETL_DIR, "page_3.json")
BOTTLENECK_TXT_PATH = os.path.join(ETL_DIR, "bottleneck.txt")
QUERY_CYPHER_PATH = os.path.join(ETL_DIR, "query.cypher")

def test_process_go_exists():
    assert os.path.isfile(PROCESS_GO_PATH), f"Go script {PROCESS_GO_PATH} does not exist."

def test_page_3_json_output():
    assert os.path.isfile(PAGE_3_JSON_PATH), f"Output file {PAGE_3_JSON_PATH} does not exist."

    with open(RAW_JSON_PATH, "r") as f:
        raw_data = json.load(f)

    # Recompute the expected result
    filtered = [a for a in raw_data if a.get("trust_score", 0) >= 0.6]
    # Sort by pagerank DESC, then author_id ASC
    sorted_data = sorted(filtered, key=lambda x: (-x.get("pagerank", 0), x.get("author_id", "")))

    # Page 3 (items 11-15, 0-indexed: 10 to 14)
    expected_page_3 = sorted_data[10:15]

    with open(PAGE_3_JSON_PATH, "r") as f:
        try:
            actual_page_3 = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {PAGE_3_JSON_PATH} does not contain valid JSON.")

    assert isinstance(actual_page_3, list), "Output should be a JSON array."
    assert len(actual_page_3) == len(expected_page_3), f"Expected {len(expected_page_3)} items in page 3, got {len(actual_page_3)}."

    for i, (actual, expected) in enumerate(zip(actual_page_3, expected_page_3)):
        assert actual.get("author_id") == expected.get("author_id"), f"Mismatch at index {i}: expected author_id {expected.get('author_id')}, got {actual.get('author_id')}."

def test_bottleneck_txt():
    assert os.path.isfile(BOTTLENECK_TXT_PATH), f"File {BOTTLENECK_TXT_PATH} does not exist."
    with open(BOTTLENECK_TXT_PATH, "r") as f:
        content = f.read().strip()

    # The operator with the highest EstimatedRows (250000) is CartesianProduct.
    # Allow optional '+' prefix if they included it, though 'CartesianProduct' is the exact name.
    assert "CartesianProduct" in content, f"Expected 'CartesianProduct' in {BOTTLENECK_TXT_PATH}, got '{content}'."

def test_query_cypher():
    assert os.path.isfile(QUERY_CYPHER_PATH), f"File {QUERY_CYPHER_PATH} does not exist."
    with open(QUERY_CYPHER_PATH, "r") as f:
        content = f.read().strip()

    assert content, f"File {QUERY_CYPHER_PATH} is empty."

    # Check for key Cypher components
    upper_content = content.upper()
    assert "MATCH" in upper_content, "Query must contain MATCH statement."
    assert "RETURN" in upper_content, "Query must contain RETURN statement."

    # Check for node and relationship patterns
    assert re.search(r'\(\s*\w*\s*:\s*Person\s*\)', content), "Query must match a Person node."
    assert re.search(r'\(\s*\w*\s*:\s*Article\s*\)', content), "Query must match an Article node."
    assert re.search(r'\[\s*\w*\s*:\s*WROTE\s*\]', content), "Query must match a WROTE relationship."

    # Check for the filter condition
    assert ">" in content and "2023" in content, "Query must filter for publish_year > 2023."
    assert "publish_year" in content, "Query must check the publish_year property."

    # Check for return fields
    assert "author_id" in content, "Query must alias id as author_id."
    assert "name" in content, "Query must return name."
    assert "pagerank" in content, "Query must return pagerank."
    assert "trust_score" in content, "Query must return trust_score."