# test_final_state.py

import os
import sqlite3
import json
import csv
from collections import defaultdict

def compute_expected_data():
    events_file = '/home/user/data/events.jsonl'
    db_file = '/home/user/data/users.db'

    # Read events
    user_scores = defaultdict(list)
    with open(events_file, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get('event_type') == 'level_complete':
                user_scores[event['user_id']].append(event['score'])

    # Calculate top 3 sum
    user_top3 = {}
    for uid, scores in user_scores.items():
        user_top3[uid] = sum(sorted(scores, reverse=True)[:3])

    # Read users
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('SELECT user_id, region FROM users')
    user_regions = {row[0]: row[1] for row in c.fetchall()}
    conn.close()

    # Join
    region_users = defaultdict(list)
    for uid, score in user_top3.items():
        region = user_regions.get(uid)
        if region:
            region_users[region].append({'user_id': uid, 'score': score})

    # Calculate rank and total
    final_data = []
    region_totals = {}
    for region, users in region_users.items():
        total_score = sum(u['score'] for u in users)
        region_totals[region] = total_score

        # Sort users by score desc to calculate rank
        users.sort(key=lambda x: x['score'], reverse=True)

        rank = 1
        for i, u in enumerate(users):
            if i > 0 and users[i]['score'] < users[i-1]['score']:
                rank = i + 1
            final_data.append({
                'region': region,
                'user_id': u['user_id'],
                'user_top3_score': u['score'],
                'region_rank': rank,
                'region_total_score': total_score
            })

    # Sort final data
    final_data.sort(key=lambda x: (x['region'], x['region_rank']))

    # Summary
    total_users_processed = len(user_top3)
    if region_totals:
        top_region = max(region_totals.items(), key=lambda x: x[1])[0]
        top_region_score = region_totals[top_region]
    else:
        top_region = None
        top_region_score = 0

    summary = {
        "total_users_processed": total_users_processed,
        "top_region": top_region,
        "top_region_score": top_region_score
    }

    return final_data, summary

def test_csv_output():
    csv_file = '/home/user/output/region_leaderboard.csv'
    assert os.path.isfile(csv_file), f"Expected CSV output file not found at {csv_file}"

    expected_data, _ = compute_expected_data()

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        actual_data = list(reader)

    assert reader.fieldnames == ['region', 'user_id', 'user_top3_score', 'region_rank', 'region_total_score'], \
        "CSV header does not match expected columns"

    assert len(actual_data) == len(expected_data), \
        f"Expected {len(expected_data)} rows in CSV, but found {len(actual_data)}"

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual['region'] == expected['region'], f"Row {i+1} region mismatch"
        assert actual['user_id'] == expected['user_id'], f"Row {i+1} user_id mismatch"
        assert int(actual['user_top3_score']) == expected['user_top3_score'], f"Row {i+1} user_top3_score mismatch"
        assert int(actual['region_rank']) == expected['region_rank'], f"Row {i+1} region_rank mismatch"
        assert int(actual['region_total_score']) == expected['region_total_score'], f"Row {i+1} region_total_score mismatch"

def test_json_output():
    json_file = '/home/user/output/etl_summary.json'
    assert os.path.isfile(json_file), f"Expected JSON output file not found at {json_file}"

    _, expected_summary = compute_expected_data()

    with open(json_file, 'r') as f:
        try:
            actual_summary = json.load(f)
        except json.JSONDecodeError:
            assert False, "etl_summary.json is not a valid JSON file"

    assert actual_summary.get('total_users_processed') == expected_summary['total_users_processed'], \
        "total_users_processed mismatch in JSON summary"
    assert actual_summary.get('top_region') == expected_summary['top_region'], \
        "top_region mismatch in JSON summary"
    assert actual_summary.get('top_region_score') == expected_summary['top_region_score'], \
        "top_region_score mismatch in JSON summary"