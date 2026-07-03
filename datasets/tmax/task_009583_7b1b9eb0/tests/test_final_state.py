# test_final_state.py

import os
import json
import sqlite3
import pytest

def get_expected_top_nodes():
    db_path = '/home/user/graph.db'
    if not os.path.isfile(db_path):
        pytest.fail(f"Database file missing: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = """
    WITH TwoHop AS (
        SELECT n.type, n.id as src_id, n2.id as dst_id
        FROM nodes n
        JOIN edges e1 ON n.id = e1.src
        JOIN edges e2 ON e1.dst = e2.src
        JOIN nodes n2 ON e2.dst = n2.id
    ),
    Aggregated AS (
        SELECT type, src_id as id, COUNT(DISTINCT dst_id) as ext_degree
        FROM TwoHop
        GROUP BY type, src_id
    )
    SELECT type, id, ext_degree,
           RANK() OVER(PARTITION BY type ORDER BY ext_degree DESC, id ASC) as rnk
    FROM Aggregated
    """

    try:
        c.execute(query)
        results = [dict(row) for row in c.fetchall()]
    except sqlite3.Error as e:
        conn.close()
        pytest.fail(f"Failed to query database to compute expected state: {e}")
    conn.close()

    expected = []
    for r in results:
        if r['rnk'] == 1:
            del r['rnk']
            expected.append(r)

    # Sort the expected list for deterministic comparison
    expected.sort(key=lambda x: (x['type'], x['id']))
    return expected

def test_top_nodes_json_exists_and_valid():
    json_path = '/home/user/top_nodes.json'
    assert os.path.isfile(json_path), f"Output file missing: {json_path}"

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert isinstance(data, list), f"JSON root must be an array, got {type(data).__name__}"

def test_top_nodes_json_correctness():
    json_path = '/home/user/top_nodes.json'
    if not os.path.isfile(json_path):
        pytest.skip("Output file missing")

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Output file is not valid JSON")

    expected = get_expected_top_nodes()

    # Check structure
    for item in data:
        assert isinstance(item, dict), "Each item in the JSON array must be an object."
        assert set(item.keys()) == {'type', 'id', 'ext_degree'}, (
            f"Object keys must be exactly 'type', 'id', 'ext_degree'. Found: {list(item.keys())}"
        )

    # Sort actual list for deterministic comparison
    data_sorted = sorted(data, key=lambda x: (x.get('type', ''), x.get('id', 0)))

    assert len(data_sorted) == len(expected), (
        f"Expected {len(expected)} top nodes, but found {len(data_sorted)}."
    )

    for actual_item, expected_item in zip(data_sorted, expected):
        assert actual_item == expected_item, (
            f"Mismatch in top nodes. Expected: {expected_item}, Actual: {actual_item}"
        )