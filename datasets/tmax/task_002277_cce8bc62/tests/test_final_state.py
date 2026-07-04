# test_final_state.py

import os
import time
import json
import sqlite3
import pytest
import requests
import networkx as nx
import redis

def get_ground_truth():
    """Compute the ground truth top 10 PageRank nodes directly from the database."""
    db_path = '/app/graph.db'
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT source, target FROM edges WHERE weight >= 0.85")
    edges = c.fetchall()
    conn.close()

    G = nx.DiGraph()
    G.add_edges_from(edges)
    pr = nx.pagerank(G)
    # Sort by PageRank score descending, then by node ID to ensure deterministic order if there are ties
    # Typically PageRank scores are unique enough, but sorting by ID as a tie-breaker is safer
    top_10 = sorted(pr.keys(), key=lambda k: (pr[k], k), reverse=True)[:10]
    return top_10

def test_db_index_created():
    """Check that an index was created on the edges table to optimize the query."""
    conn = sqlite3.connect('/app/graph.db')
    c = conn.cursor()
    c.execute("PRAGMA index_list('edges');")
    indices = c.fetchall()

    has_useful_index = False
    for idx in indices:
        idx_name = idx[1]
        c.execute(f"PRAGMA index_info('{idx_name}');")
        columns = [row[2] for row in c.fetchall()]
        # The query filters by weight, so an index starting with weight is optimal
        if columns and columns[0] == 'weight':
            has_useful_index = True
            break

    conn.close()
    assert has_useful_index, "No index starting with 'weight' was found on the 'edges' table. The query will still be slow."

def test_pagerank_endpoint_and_cache():
    """
    Test the /pagerank endpoint for correctness, speed, and caching behavior.
    """
    # 1. Clear Redis cache
    r = redis.Redis(host='localhost', port=6379, db=0)
    try:
        r.ping()
    except redis.ConnectionError:
        pytest.fail("Redis server is not running or not accessible on localhost:6379")

    r.flushdb()

    # 2. Compute ground truth
    ground_truth = get_ground_truth()

    # 3. Call the endpoint and measure time
    start_time = time.time()
    try:
        resp = requests.get('http://localhost:5000/pagerank', timeout=5.0)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to etl_api.py on port 5000: {e}")

    elapsed = time.time() - start_time

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"

    try:
        result = resp.json()
    except ValueError:
        pytest.fail("Endpoint did not return valid JSON")

    # 4. Assert response time is acceptable (< 3.0s)
    assert elapsed < 3.0, f"Endpoint response time too slow: {elapsed:.2f}s (Threshold: 3.0s). Did you create the correct index?"

    # 5. Check accuracy
    assert isinstance(result, list), "Expected a JSON array (list)"
    assert len(result) == 10, f"Expected exactly 10 nodes, got {len(result)}"

    set_result = set(result)
    set_truth = set(ground_truth)

    intersection = len(set_result.intersection(set_truth))
    union = len(set_result.union(set_truth))
    accuracy = intersection / union if union > 0 else 0.0

    assert accuracy == 1.0, f"Accuracy metric failed. Expected Jaccard similarity of 1.0, got {accuracy:.2f}. Returned: {result}, Expected: {ground_truth}"

    # 6. Check Redis cache
    cached_val = r.get('top_pagerank')
    assert cached_val is not None, "The key 'top_pagerank' was not found in Redis."

    try:
        cached_list = json.loads(cached_val)
    except ValueError:
        pytest.fail("Cached value in Redis is not valid JSON.")

    assert cached_list == result, "Cached list in Redis does not match the returned list."

    ttl = r.ttl('top_pagerank')
    assert 0 < ttl <= 60, f"Expected TTL between 1 and 60 seconds, got {ttl}"