# test_final_state.py

import os
import pandas as pd
import pytest

def test_edges_appended():
    """Test that the 3 missing edges were appended to edges.csv."""
    edges_file = "/home/user/edges.csv"
    assert os.path.isfile(edges_file), f"File {edges_file} is missing."

    df = pd.read_csv(edges_file)

    # Required edges from the audio file
    required_edges = [
        (400, 500, 20),
        (500, 600, 30),
        (600, 700, 40)
    ]

    for u, v, w in required_edges:
        match = df[(df['source'] == u) & (df['target'] == v) & (df['weight'] == w)]
        assert not match.empty, f"Missing required edge in edges.csv: source={u}, target={v}, weight={w}"

def test_final_results_accuracy():
    """Test that the final results match the golden 2-hop path computation."""
    final_results_file = "/home/user/final_results.csv"
    assert os.path.isfile(final_results_file), f"File {final_results_file} is missing."

    edges_file = "/home/user/edges.csv"
    edges_df = pd.read_csv(edges_file)

    # Build adjacency list
    adj = {}
    for _, row in edges_df.iterrows():
        u, v, w = int(row['source']), int(row['target']), float(row['weight'])
        if u not in adj:
            adj[u] = []
        adj[u].append((v, w))

    # Compute max 2-hop paths
    two_hop = {}
    for u in adj:
        for v, w1 in adj[u]:
            if v in adj:
                for c, w2 in adj[v]:
                    if u != c:
                        total_w = w1 + w2
                        if (u, c) not in two_hop or total_w > two_hop[(u, c)]:
                            two_hop[(u, c)] = total_w

    # Create golden dataframe
    results = [{'source': u, 'target': c, 'total_weight': w} for (u, c), w in two_hop.items()]
    golden_df = pd.DataFrame(results)

    # Sort: total_weight DESC, source ASC, target ASC
    golden_df = golden_df.sort_values(
        by=['total_weight', 'source', 'target'], 
        ascending=[False, True, True]
    ).reset_index(drop=True)

    # Pagination limit from audio
    golden_df = golden_df.head(15)

    # Evaluate agent results
    try:
        agent_df = pd.read_csv(final_results_file)
    except Exception as e:
        pytest.fail(f"Failed to read {final_results_file}: {e}")

    if len(agent_df) != len(golden_df):
        accuracy = 0.0
    else:
        matches = 0
        for i in range(len(golden_df)):
            if (agent_df.iloc[i]['source'] == golden_df.iloc[i]['source'] and 
                agent_df.iloc[i]['target'] == golden_df.iloc[i]['target'] and 
                abs(agent_df.iloc[i]['total_weight'] - golden_df.iloc[i]['total_weight']) < 1e-6):
                matches += 1
        accuracy = matches / len(golden_df)

    assert accuracy >= 0.99, f"Accuracy {accuracy} is below the 0.99 threshold. Expected {len(golden_df)} exact row matches."