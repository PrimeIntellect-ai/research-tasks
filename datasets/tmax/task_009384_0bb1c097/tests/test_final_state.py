# test_final_state.py

import os
import json
import sqlite3
import csv
import pytest

DB_PATH = '/home/user/sensor_data.db'
QUERY_PLAN_PATH = '/home/user/query_plan.txt'
JSON_OUTPUT_PATH = '/home/user/aggregated_output.json'
SENSORS_CSV = '/home/user/sensors.csv'
READINGS_CSV = '/home/user/readings.csv'

def test_database_exists():
    assert os.path.isfile(DB_PATH), f"Database file missing: {DB_PATH}"

def test_tables_and_indexes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    assert 'sensors' in tables, "Table 'sensors' is missing from the database."
    assert 'readings' in tables, "Table 'readings' is missing from the database."

    # Check indexes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name IN ('sensors', 'readings')")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No indexes found on 'sensors' or 'readings' tables."

    conn.close()

def test_query_plan():
    assert os.path.isfile(QUERY_PLAN_PATH), f"Query plan file missing: {QUERY_PLAN_PATH}"
    with open(QUERY_PLAN_PATH, 'r') as f:
        plan = f.read().upper()

    assert "INDEX" in plan, "Query plan does not indicate the use of an index."

def test_json_output_structure_and_values():
    assert os.path.isfile(JSON_OUTPUT_PATH), f"JSON output file missing: {JSON_OUTPUT_PATH}"

    with open(JSON_OUTPUT_PATH, 'r') as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON.")

    assert isinstance(output_data, list), "JSON output must be a list of objects."

    # Compute expected results from CSVs
    sensors = {}
    with open(SENSORS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensors[row['sensor_id']] = row

    latest_readings = {}
    with open(READINGS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            s_id = row['sensor_id']
            if s_id not in sensors:
                continue
            loc = sensors[s_id]['location_id']
            stype = sensors[s_id]['sensor_type']
            key = (loc, stype)

            if key not in latest_readings or row['timestamp'] > latest_readings[key]['latest_timestamp']:
                latest_readings[key] = {
                    'location_id': loc,
                    'sensor_type': stype,
                    'latest_timestamp': row['timestamp'],
                    'reading_value': float(row['reading_value'])
                }

    expected_list = list(latest_readings.values())

    assert len(output_data) == len(expected_list), f"Expected {len(expected_list)} items in JSON output, got {len(output_data)}."

    expected_dict = {(d['location_id'], d['sensor_type']): d for d in expected_list}

    for item in output_data:
        assert isinstance(item, dict), "Items in JSON list must be objects."
        keys = {'location_id', 'sensor_type', 'latest_timestamp', 'reading_value'}
        assert set(item.keys()) == keys, f"JSON object keys must be exactly {keys}."

        key = (item['location_id'], item['sensor_type'])
        assert key in expected_dict, f"Unexpected location/sensor combination: {key}"

        expected_item = expected_dict[key]
        assert item['latest_timestamp'] == expected_item['latest_timestamp'], f"Incorrect timestamp for {key}"
        assert float(item['reading_value']) == expected_item['reading_value'], f"Incorrect reading value for {key}"