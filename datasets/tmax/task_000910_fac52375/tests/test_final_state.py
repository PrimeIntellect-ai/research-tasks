# test_final_state.py

import os
import csv
import pytest

def get_csv_data(filepath):
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def test_cypher_script_content():
    cypher_path = '/home/user/graph.cypher'
    assert os.path.isfile(cypher_path), f"The file {cypher_path} is missing."

    cities = get_csv_data('/home/user/data/cities.csv')
    users = get_csv_data('/home/user/data/users.csv')
    friendships = get_csv_data('/home/user/data/friendships.csv')

    # Sort data
    cities.sort(key=lambda x: int(x['id']))
    users.sort(key=lambda x: int(x['id']))

    expected_lines = []

    # 1. Cities
    for c in cities:
        expected_lines.append(f"CREATE (:City {{id: {c['id']}, name: '{c['name']}'}});")

    # 2. Users
    for u in users:
        expected_lines.append(f"CREATE (:User {{id: {u['id']}, name: '{u['name']}'}});")

    # 3. LIVES_IN
    for u in users:
        expected_lines.append(f"MATCH (u:User {{id: {u['id']}}}), (c:City {{id: {u['city_id']}}}) CREATE (u)-[:LIVES_IN]->(c);")

    # 4. KNOWS
    knows_set = set()
    for f in friendships:
        u1, u2 = int(f['user1_id']), int(f['user2_id'])
        knows_set.add((u1, u2))
        knows_set.add((u2, u1))

    knows_list = sorted(list(knows_set))
    for u1, u2 in knows_list:
        expected_lines.append(f"MATCH (u1:User {{id: {u1}}}), (u2:User {{id: {u2}}}) CREATE (u1)-[:KNOWS]->(u2);")

    with open(cypher_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {cypher_path}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {cypher_path} is incorrect.\nExpected: {expected}\nActual:   {actual}"

def test_answer_txt_content():
    answer_path = '/home/user/answer.txt'
    assert os.path.isfile(answer_path), f"The file {answer_path} is missing."

    cities = get_csv_data('/home/user/data/cities.csv')
    users = get_csv_data('/home/user/data/users.csv')
    friendships = get_csv_data('/home/user/data/friendships.csv')

    # Build graphs
    city_map = {c['id']: c['name'] for c in cities}
    user_map = {u['id']: u for u in users}

    adj = {u['id']: set() for u in users}
    for f in friendships:
        u1, u2 = f['user1_id'], f['user2_id']
        adj[u1].add(u2)
        adj[u2].add(u1)

    # Find Alice
    alice_id = None
    for u in users:
        if u['name'] == 'Alice':
            alice_id = u['id']
            break

    assert alice_id is not None, "Alice not found in users.csv"

    # 1 hop
    friends = adj[alice_id]

    # 2 hops
    fof = set()
    for friend in friends:
        fof.update(adj[friend])

    # Exclude Alice and direct friends
    fof.discard(alice_id)
    fof -= friends

    # Filter by city Graphville
    graphville_id = None
    for c in cities:
        if c['name'] == 'Graphville':
            graphville_id = c['id']
            break

    valid_fof_names = []
    for uid in fof:
        if user_map[uid]['city_id'] == graphville_id:
            valid_fof_names.append(user_map[uid]['name'])

    assert len(valid_fof_names) == 1, "Expected exactly one valid friend-of-a-friend"
    expected_answer = valid_fof_names[0]

    with open(answer_path, 'r') as f:
        actual_answer = f.read().strip()

    assert actual_answer == expected_answer, f"Expected answer '{expected_answer}', but got '{actual_answer}'"