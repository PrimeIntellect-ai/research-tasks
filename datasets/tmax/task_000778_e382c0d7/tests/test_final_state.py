# test_final_state.py

import os
import csv
import sqlite3
import math
import re
import pytest

def compute_ground_truth():
    log_path = '/home/user/raw_logs.csv'
    if not os.path.exists(log_path):
        return []

    users = {}
    with open(log_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row['user_id']
            if uid not in users:
                users[uid] = {'req': 0, 'ips': set(), 'bytes': []}
            users[uid]['req'] += 1
            users[uid]['ips'].add(row['source_ip'])
            users[uid]['bytes'].append(int(row['bytes_sent']))

    baseline = [50, 1, 2500]
    baseline_norm = math.sqrt(sum(x*x for x in baseline))

    results = []
    for uid, data in users.items():
        req = data['req']
        ips = len(data['ips'])
        avg_b = sum(data['bytes']) / req
        vec = [req, ips, avg_b]
        vec_norm = math.sqrt(sum(x*x for x in vec))
        dot = sum(a*b for a, b in zip(baseline, vec))
        sim = dot / (baseline_norm * vec_norm) if vec_norm > 0 else 0.0
        results.append({
            'user_id': uid,
            'total_requests': req,
            'unique_ips': ips,
            'avg_bytes': avg_b,
            'similarity_score': sim
        })

    results.sort(key=lambda x: x['similarity_score'])
    return results[:5]

def test_database_bulk_import():
    db_path = '/home/user/logs.db'
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='access_logs';")
    table_exists = cursor.fetchone()
    assert table_exists, "Table 'access_logs' does not exist in the database."

    cursor.execute("SELECT COUNT(*) FROM access_logs;")
    count = cursor.fetchone()[0]
    assert count > 0, "Table 'access_logs' is empty."
    conn.close()

def test_top_anomalies_csv():
    csv_path = '/home/user/top_anomalies.csv'
    assert os.path.exists(csv_path), f"CSV file {csv_path} does not exist."

    expected_top5 = compute_ground_truth()
    assert len(expected_top5) == 5, "Could not compute ground truth."

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 5, f"Expected exactly 5 rows in {csv_path}, found {len(rows)}."

    expected_cols = {'user_id', 'total_requests', 'unique_ips', 'avg_bytes', 'similarity_score'}
    assert set(reader.fieldnames) == expected_cols, f"CSV columns do not match expected. Got {reader.fieldnames}"

    for i, (actual, expected) in enumerate(zip(rows, expected_top5)):
        assert actual['user_id'] == expected['user_id'], f"Row {i+1} user_id mismatch. Expected {expected['user_id']}, got {actual['user_id']}."
        assert int(actual['total_requests']) == expected['total_requests'], f"Row {i+1} total_requests mismatch."
        assert int(actual['unique_ips']) == expected['unique_ips'], f"Row {i+1} unique_ips mismatch."
        assert math.isclose(float(actual['avg_bytes']), expected['avg_bytes'], rel_tol=1e-5), f"Row {i+1} avg_bytes mismatch."
        assert math.isclose(float(actual['similarity_score']), expected['similarity_score'], abs_tol=1e-3), f"Row {i+1} similarity_score mismatch."

def test_anomaly_report_html():
    html_path = '/home/user/anomaly_report.html'
    assert os.path.exists(html_path), f"HTML report {html_path} does not exist."

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    expected_top5 = compute_ground_truth()

    for expected in expected_top5:
        uid = expected['user_id']
        sim = round(expected['similarity_score'], 4)

        # We allow some flexibility in whitespace, but the structure must match
        pattern = rf"<li>User\s+{uid}\s+with score\s+{sim}0*</li>"
        match = re.search(pattern, content)
        assert match, f"Could not find expected <li> tag for user {uid} with score ~{sim} in the HTML report."