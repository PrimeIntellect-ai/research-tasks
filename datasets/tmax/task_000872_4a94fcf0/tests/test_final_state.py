# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/graph_backup.db"
CYPHER_PATH = "/home/user/restore.cypher"

def get_expected_cypher():
    """Dynamically compute the expected Cypher script based on the SQLite DB contents."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Retrieve all nodes
    cursor.execute("SELECT id, hostname, region FROM nodes")
    nodes = cursor.fetchall()

    # Retrieve all edges
    cursor.execute("SELECT source_id, target_id, latency FROM edges")
    edges = cursor.fetchall()

    # Calculate out-degree and sum of latencies for each node
    out_stats = {n['id']: {'count': 0, 'sum_latency': 0.0} for n in nodes}

    for e in edges:
        src = e['source_id']
        if src in out_stats:
            out_stats[src]['count'] += 1
            out_stats[src]['sum_latency'] += e['latency']

    # Group nodes by region
    regions = {}
    for n in nodes:
        reg = n['region']
        if reg not in regions:
            regions[reg] = []
        regions[reg].append({
            'id': n['id'],
            'hostname': n['hostname'],
            'region': n['region'],
            'out_count': out_stats[n['id']]['count'],
            'sum_latency': out_stats[n['id']]['sum_latency']
        })

    core_servers = []
    for reg, srvs in regions.items():
        # Sort by out_count DESC, id ASC
        srvs.sort(key=lambda x: (-x['out_count'], x['id']))
        # Take top 2
        core_servers.extend(srvs[:2])

    # Sort the core servers by ID ASC for the node creation statements
    core_servers.sort(key=lambda x: x['id'])
    core_ids = {s['id'] for s in core_servers}

    # Generate CREATE node statements
    node_statements = []
    for s in core_servers:
        avg_lat = 0.0
        if s['out_count'] > 0:
            avg_lat = round(s['sum_latency'] / s['out_count'], 1)
        stmt = f"CREATE (:Server {{id: {s['id']}, hostname: '{s['hostname']}', region: '{s['region']}', avg_out_latency: {avg_lat}}});"
        node_statements.append(stmt)

    # Generate MATCH ... CREATE edge statements
    edge_statements = []
    core_edges = [e for e in edges if e['source_id'] in core_ids and e['target_id'] in core_ids]
    # Sort by source_id ASC, target_id ASC
    core_edges.sort(key=lambda x: (x['source_id'], x['target_id']))

    for e in core_edges:
        stmt = f"MATCH (s:Server {{id: {e['source_id']}}}), (t:Server {{id: {e['target_id']}}}) CREATE (s)-[:CONNECTS_TO {{latency: {e['latency']}}}]->(t);"
        edge_statements.append(stmt)

    expected_lines = node_statements + [""] + edge_statements
    expected_content = "\n".join(expected_lines)

    conn.close()
    return expected_content

def test_restore_cypher_exists():
    """Verify that the expected Cypher file exists."""
    assert os.path.isfile(CYPHER_PATH), f"File {CYPHER_PATH} does not exist."

def test_restore_cypher_contents():
    """Verify that the Cypher file contains the correctly formatted statements based on the DB state."""
    expected = get_expected_cypher()
    with open(CYPHER_PATH, 'r') as f:
        actual = f.read()

    # We strip trailing whitespace to avoid failing on trivial newline differences at EOF
    assert actual.strip() == expected.strip(), (
        f"Contents of {CYPHER_PATH} do not match the expected output.\n"
        f"Expected:\n{expected.strip()}\n\n"
        f"Actual:\n{actual.strip()}"
    )