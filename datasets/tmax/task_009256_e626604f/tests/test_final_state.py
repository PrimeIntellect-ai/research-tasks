import os
import json
import sqlite3
import pytest

OUTPUT_PATH = '/home/user/output/key_communicators.json'
DB_PATH = '/home/user/data/comms.db'

def compute_pagerank(nodes, edges, alpha=0.85, max_iter=100, tol=1.0e-6):
    """
    Computes PageRank exactly as NetworkX does for weighted directed graphs.
    nodes: list of node IDs
    edges: dict of sender_id -> {receiver_id: weight}
    """
    N = len(nodes)
    if N == 0:
        return {}

    out_weight = {u: sum(edges.get(u, {}).values()) for u in nodes}
    x = {u: 1.0 / N for u in nodes}

    # NetworkX distributes dangling node mass to all nodes
    for _ in range(max_iter):
        xlast = x.copy()
        x = {u: 0.0 for u in nodes}
        danglesum = alpha * sum(xlast[u] for u in nodes if out_weight[u] == 0)

        for u in nodes:
            for v, w in edges.get(u, {}).items():
                x[v] += alpha * xlast[u] * w / out_weight[u]
            x[u] += danglesum / N + (1.0 - alpha) / N

        err = sum(abs(x[u] - xlast[u]) for u in nodes)
        if err < tol:
            break

    return x

def get_truth_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch users and departments
    cursor.execute("""
        SELECT u.id, u.name, d.name 
        FROM users u 
        JOIN departments d ON u.department_id = d.id
    """)
    users = {row[0]: {'name': row[1], 'department_name': row[2]} for row in cursor.fetchall()}

    # Fetch messages to compute sent counts and graph edges
    cursor.execute("SELECT sender_id, receiver_id FROM messages")
    messages = cursor.fetchall()
    conn.close()

    # Compute messages sent
    sent_counts = {u: 0 for u in users}
    for sender, _ in messages:
        if sender in sent_counts:
            sent_counts[sender] += 1

    # Compute department ranks
    dept_users = {}
    for uid, uinfo in users.items():
        dept = uinfo['department_name']
        dept_users.setdefault(dept, []).append((uid, sent_counts[uid]))

    dept_ranks = {}
    for dept, ulist in dept_users.items():
        # Sort by sent count descending
        ulist.sort(key=lambda x: x[1], reverse=True)
        rank = 1
        for i, (uid, count) in enumerate(ulist):
            if i > 0 and count < ulist[i-1][1]:
                rank = i + 1
            dept_ranks[uid] = rank

    # Compute graph edges
    nodes = list(users.keys())
    edges = {}
    for sender, receiver in messages:
        if sender not in edges:
            edges[sender] = {}
        edges[sender][receiver] = edges[sender].get(receiver, 0) + 1

    pageranks = compute_pagerank(nodes, edges)

    # Combine data
    results = []
    for uid in users:
        results.append({
            "user_id": uid,
            "name": users[uid]['name'],
            "department_name": users[uid]['department_name'],
            "messages_sent": sent_counts[uid],
            "dept_rank": dept_ranks[uid],
            "pagerank": round(pageranks[uid], 4)
        })

    # Sort by pagerank descending
    results.sort(key=lambda x: x['pagerank'], reverse=True)
    return results[:3]

def test_output_file_exists():
    assert os.path.exists(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH}"
    assert os.path.isfile(OUTPUT_PATH), f"Path {OUTPUT_PATH} is not a file"

def test_output_json_format_and_values():
    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON")

    assert isinstance(data, list), "JSON output must be a list of dictionaries"
    assert len(data) == 3, f"Expected exactly 3 users in output, got {len(data)}"

    truth_data = get_truth_data()

    for i, (actual, expected) in enumerate(zip(data, truth_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a dictionary"

        expected_keys = {"user_id", "name", "department_name", "messages_sent", "dept_rank", "pagerank"}
        assert set(actual.keys()) == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, got {set(actual.keys())}"

        assert actual["user_id"] == expected["user_id"], f"Rank {i+1}: Expected user_id {expected['user_id']}, got {actual['user_id']}"
        assert actual["name"] == expected["name"], f"Rank {i+1}: Expected name {expected['name']}, got {actual['name']}"
        assert actual["department_name"] == expected["department_name"], f"Rank {i+1}: Expected dept {expected['department_name']}, got {actual['department_name']}"
        assert actual["messages_sent"] == expected["messages_sent"], f"Rank {i+1}: Expected messages_sent {expected['messages_sent']}, got {actual['messages_sent']}"
        assert actual["dept_rank"] == expected["dept_rank"], f"Rank {i+1}: Expected dept_rank {expected['dept_rank']}, got {actual['dept_rank']}"

        # Allow small floating point differences due to potential networkx version differences
        assert abs(actual["pagerank"] - expected["pagerank"]) <= 0.0002, \
            f"Rank {i+1}: Expected pagerank ~{expected['pagerank']}, got {actual['pagerank']}"