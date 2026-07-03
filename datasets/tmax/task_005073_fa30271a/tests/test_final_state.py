# test_final_state.py

import os
import subprocess
import pandas as pd
import numpy as np

def test_metric_top_nodes_mae():
    agent_file = "/home/user/top_nodes.csv"
    assert os.path.exists(agent_file), f"Agent output file missing at {agent_file}"

    agent_df = pd.read_csv(agent_file)
    assert len(agent_df) == 20, f"Expected 20 rows in {agent_file}, got {len(agent_df)}"
    assert {'node_id', 'pagerank_score'}.issubset(agent_df.columns), "Missing required columns in agent output"

    truth_file = "/app/reference_top_nodes.csv"
    assert os.path.exists(truth_file), f"Reference file missing at {truth_file}"
    truth_df = pd.read_csv(truth_file)

    merged = pd.merge(truth_df, agent_df, on="node_id", suffixes=('_ref', '_agent'), how='left')
    merged['pagerank_score_agent'] = merged['pagerank_score_agent'].fillna(0.0)

    mae = np.mean(np.abs(merged['pagerank_score_ref'] - merged['pagerank_score_agent']))

    assert mae <= 1e-4, f"MAE {mae:.6f} exceeds threshold 1e-4"

def test_redis_hash_populated():
    # Query Redis to verify the 'node_pageranks' Hash has been populated
    try:
        result = subprocess.run(
            ["redis-cli", "HLEN", "node_pageranks"], 
            capture_output=True, text=True, check=True
        )
        hlen = int(result.stdout.strip())
        assert hlen > 0, "Redis hash 'node_pageranks' is empty or does not exist"
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to query Redis: {e.stderr}"

def test_postgres_database_and_table():
    # Verify database exists
    try:
        result_db = subprocess.run(
            ["psql", "-U", "postgres", "-lqt"], 
            capture_output=True, text=True, check=True
        )
        assert "graph_analytics" in result_db.stdout, "Database 'graph_analytics' does not exist"
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to list PostgreSQL databases: {e.stderr}"

    # Verify raw_interactions table exists and is populated
    query = "SELECT COUNT(*) FROM raw_interactions;"
    try:
        result_table = subprocess.run(
            ["psql", "-U", "postgres", "-d", "graph_analytics", "-t", "-c", query], 
            capture_output=True, text=True, check=True
        )
        count = int(result_table.stdout.strip())
        assert count > 0, "Table 'raw_interactions' is empty"
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to query 'raw_interactions' table: {e.stderr}"

def test_python_script_exists():
    script_path = "/home/user/process_graph.py"
    assert os.path.exists(script_path), f"Python script missing at {script_path}"
    assert os.path.isfile(script_path), f"Path {script_path} is not a file"