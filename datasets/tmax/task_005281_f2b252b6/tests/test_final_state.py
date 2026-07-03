# test_final_state.py

import os
import time
import subprocess
import json
import urllib.request
import base64
import pandas as pd

def query_neo4j(statement):
    url = "http://localhost:7474/db/neo4j/tx/commit"
    data = json.dumps({"statements": [{"statement": statement}]}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.b64encode(b"neo4j:password123").decode('utf-8')
    })
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            return json.loads(res_body)
    except Exception as e:
        raise RuntimeError(f"Neo4j query failed: {e}")

def clear_neo4j():
    query_neo4j("MATCH (n) DETACH DELETE n")

def count_neo4j_nodes():
    res = query_neo4j("MATCH (n) RETURN count(n)")
    return res["results"][0]["data"][0]["row"][0]

def count_neo4j_edges():
    res = query_neo4j("MATCH ()-[r]->() RETURN count(r)")
    return res["results"][0]["data"][0]["row"][0]

def test_etl_speedup():
    fast_etl_path = "/home/user/fast_etl.py"
    naive_etl_path = "/app/naive_etl.py"

    assert os.path.exists(fast_etl_path), f"Fast ETL script not found at {fast_etl_path}"
    assert os.path.exists(naive_etl_path), f"Naive ETL script not found at {naive_etl_path}"

    # 1. Clean Neo4j
    clear_neo4j()

    # 2. Measure Naive
    start = time.time()
    subprocess.run(["python3", naive_etl_path], check=True)
    t_naive = time.time() - start
    naive_nodes = count_neo4j_nodes()
    naive_edges = count_neo4j_edges()

    # 3. Clean Neo4j
    clear_neo4j()

    # 4. Measure Fast
    start = time.time()
    subprocess.run(["python3", fast_etl_path], check=True)
    t_fast = time.time() - start
    fast_nodes = count_neo4j_nodes()
    fast_edges = count_neo4j_edges()

    assert fast_nodes > 0, "Fast ETL script did not load any nodes into Neo4j."
    assert fast_nodes == naive_nodes, f"Fast ETL loaded {fast_nodes} nodes, expected {naive_nodes}."
    assert fast_edges == naive_edges, f"Fast ETL loaded {fast_edges} edges, expected {naive_edges}."

    speedup = t_naive / t_fast
    assert speedup >= 15.0, f"Speedup {speedup:.2f} is below threshold 15.0 (Naive: {t_naive:.2f}s, Fast: {t_fast:.2f}s)"

def test_centrality_csv():
    csv_path = "/home/user/centrality.csv"
    assert os.path.exists(csv_path), f"Analytics output not found at {csv_path}"

    df = pd.read_csv(csv_path)
    assert list(df.columns) == ["user_id", "out_degree"], f"Incorrect columns in {csv_path}: {list(df.columns)}"

    if len(df) > 1:
        # Check descending order for out_degree
        out_degrees = df["out_degree"].tolist()
        assert out_degrees == sorted(out_degrees, reverse=True), "The out_degree column is not sorted in descending order"

        # Check secondary sort by user_id ascending
        for _, group in df.groupby("out_degree"):
            user_ids = group["user_id"].tolist()
            assert user_ids == sorted(user_ids), "The user_id column is not sorted in ascending order for ties in out_degree"