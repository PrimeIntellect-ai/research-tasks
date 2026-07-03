# test_final_state.py

import os
import sqlite3
import hashlib
from collections import defaultdict

DB_PATH = '/home/user/data/analytics.db'

def test_db_exists():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."

def test_clean_events_count_and_deduplication():
    assert os.path.isfile(DB_PATH), "Database file is missing."
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*) FROM clean_events")
        clean_count = cur.fetchone()[0]
        assert clean_count == 10000, f"Expected 10000 clean events, got {clean_count}"

        cur.execute("SELECT user_id, event_type, payload FROM clean_events")
        rows = cur.fetchall()
        seen_hashes = set()
        for r in rows:
            h = hashlib.md5(f"{r[0]}{r[1]}{r[2]}".encode('utf-8')).hexdigest()
            assert h not in seen_hashes, f"Found duplicate hash in clean_events for user_id={r[0]}, event_type={r[1]}, payload={r[2]}!"
            seen_hashes.add(h)
    finally:
        conn.close()

def test_sampled_events_stratification_and_logic():
    assert os.path.isfile(DB_PATH), "Database file is missing."
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("SELECT event_type, COUNT(*) FROM clean_events GROUP BY event_type")
        strata_counts = dict(cur.fetchall())

        cur.execute("SELECT event_type, COUNT(*) FROM sampled_events GROUP BY event_type")
        sample_counts = dict(cur.fetchall())

        for etype, count in strata_counts.items():
            expected_sample = (count + 9) // 10  # 0-indexed, every 10th record
            actual_sample = sample_counts.get(etype, 0)
            assert actual_sample == expected_sample, f"Expected {expected_sample} sampled events for {etype}, got {actual_sample}"

        cur.execute("SELECT event_type, event_id FROM sampled_events")
        sampled_ids = cur.fetchall()

        cur.execute("SELECT event_type, event_id FROM clean_events")
        all_clean = cur.fetchall()

        clean_dict = defaultdict(list)
        for et, eid in all_clean:
            clean_dict[et].append(eid)

        for et in clean_dict:
            clean_dict[et].sort()

        for et, eid in sampled_ids:
            idx = clean_dict[et].index(eid)
            assert idx % 10 == 0, f"Sampled event {eid} for type {et} is at index {idx}, which is not a multiple of 10."
    finally:
        conn.close()