# test_final_state.py

import os
import json
import csv

def test_critical_backups_csv():
    jsonl_path = "/home/user/backups.jsonl"
    csv_path = "/home/user/critical_backups.csv"

    assert os.path.isfile(jsonl_path), f"{jsonl_path} is missing."
    assert os.path.isfile(csv_path), f"Output file {csv_path} was not created."

    # Read backups
    backups = []
    with open(jsonl_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            backups.append(json.loads(line))

    # Compute children_count
    children_count = {b['id']: 0 for b in backups}
    for b in backups:
        parent_id = b.get('parent_id')
        if parent_id is not None and parent_id in children_count:
            children_count[parent_id] += 1

    # Compute region_rank
    regions = {}
    for b in backups:
        regions.setdefault(b['region'], []).append(b)

    region_ranks = {}
    for region, region_backups in regions.items():
        # sort by size_bytes descending, then id ascending
        sorted_backups = sorted(region_backups, key=lambda x: (-x['size_bytes'], x['id']))
        for rank, b in enumerate(sorted_backups, start=1):
            region_ranks[b['id']] = rank

    # Prepare expected output
    expected_rows = []
    for b in backups:
        expected_rows.append({
            'id': b['id'],
            'children_count': children_count[b['id']],
            'region_rank': region_ranks[b['id']]
        })

    # Sort by id alphabetically
    expected_rows.sort(key=lambda x: x['id'])

    expected_csv = [["id", "children_count", "region_rank"]]
    for row in expected_rows:
        expected_csv.append([row['id'], str(row['children_count']), str(row['region_rank'])])

    # Read actual CSV
    actual_csv = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if any(cell.strip() for cell in row):
                actual_csv.append([cell.strip() for cell in row])

    assert len(actual_csv) > 0, f"CSV file {csv_path} is empty."
    assert actual_csv[0] == ["id", "children_count", "region_rank"], "CSV header is incorrect."

    assert len(actual_csv) == len(expected_csv), f"Expected {len(expected_csv)} rows, got {len(actual_csv)}."

    for i, (actual, expected) in enumerate(zip(actual_csv, expected_csv)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}."