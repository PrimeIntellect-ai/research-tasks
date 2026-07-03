# test_final_state.py
import os
import sqlite3
import pytest

def get_expected_optimal_hub():
    db_path = "/home/user/logistics.db"
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT l.name, COUNT(s.shipment_id) as out_degree
    FROM locations l
    JOIN routes r ON l.loc_id = r.source_id
    JOIN shipments s ON r.route_id = s.route_id
    GROUP BY l.loc_id
    ORDER BY out_degree DESC
    LIMIT 1;
    """

    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Could not compute the optimal hub from the database."
    return result[0]

def test_optimal_hub_file():
    output_path = "/home/user/optimal_hub.txt"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    expected_hub = get_expected_optimal_hub()

    assert content == expected_hub, f"Expected optimal hub to be '{expected_hub}', but found '{content}'."