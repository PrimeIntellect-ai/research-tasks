# test_final_state.py
import os
import json
import sqlite3
from collections import deque, defaultdict
import pytest

DB_PATH = "/home/user/ecommerce.db"
JSONL_PATH = "/home/user/activity.jsonl"
REPORT_PATH = "/home/user/report.json"

def get_shortest_path(db_path, start, end):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT user_id1, user_id2 FROM friendships")
    graph = defaultdict(list)
    for u, v in c.fetchall():
        graph[u].append(v)
    conn.close()

    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == end:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return []

def get_expected_purchases(db_path, path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    purchases = {}
    for uid in path:
        c.execute("SELECT name FROM users WHERE id = ?", (uid,))
        row = c.fetchone()
        name = row[0] if row else f"User_{uid}"

        c.execute("SELECT SUM(amount) FROM purchases WHERE user_id = ?", (uid,))
        total_row = c.fetchone()
        total = total_row[0] if total_row and total_row[0] is not None else 0.0

        purchases[str(uid)] = {"name": name, "total_spent": total}
    conn.close()
    return purchases

def get_expected_activities(jsonl_path, path):
    path_set = set(path)
    activities = defaultdict(lambda: defaultdict(list))
    with open(jsonl_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            uid = record.get("user_id")
            if uid in path_set:
                activities[str(uid)][record["event"]].append(record["duration_ms"])

    aggregation = {}
    for uid, events in activities.items():
        aggregation[uid] = {}
        for event, durations in events.items():
            aggregation[uid][event] = sum(durations) / len(durations)
    return aggregation

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} was not generated."

def test_report_content():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} missing."

    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    assert "path" in report, "Key 'path' missing from report."
    assert "purchases" in report, "Key 'purchases' missing from report."
    assert "activity_aggregation" in report, "Key 'activity_aggregation' missing from report."

    expected_path = get_shortest_path(DB_PATH, 1, 20)
    assert report["path"] == expected_path, f"Expected path {expected_path}, got {report['path']}"

    expected_purchases = get_expected_purchases(DB_PATH, expected_path)
    assert report["purchases"] == expected_purchases, "Purchases aggregation does not match expected output."

    expected_activities = get_expected_activities(JSONL_PATH, expected_path)
    assert report["activity_aggregation"] == expected_activities, "Activity aggregation does not match expected output."