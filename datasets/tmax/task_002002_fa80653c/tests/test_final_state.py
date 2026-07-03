# test_final_state.py

import os
import json
import pytest
import numpy as np
import networkx as nx
import pandas as pd

def compute_golden_scores(csv_path):
    df = pd.read_csv(csv_path)
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(str(row['author_A']), str(row['author_B']), weight=float(row['collaborations']))

    # PageRank
    pr = nx.pagerank(G, alpha=0.85, weight='collaborations')

    # Clustering Coefficient
    # NetworkX average_clustering or clustering doesn't use edge weights by default in the same way,
    # but let's check standard clustering as the prompt says "Local Clustering Coefficient"
    cc = nx.clustering(G)

    scores = {}
    for node in G.nodes():
        scores[node] = 0.75 * pr[node] + 0.25 * cc[node]

    return scores

def test_fast_ranker_output():
    output_path = '/home/user/top_authors_page1.json'
    csv_path = '/home/user/dataset/coauthors.csv'

    assert os.path.exists(output_path), f"Output file {output_path} is missing"

    with open(output_path, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_path} is not valid JSON")

    assert 'results' in agent_data, "JSON missing 'results' key"
    assert 'page' in agent_data, "JSON missing 'page' key"
    assert 'page_size' in agent_data, "JSON missing 'page_size' key"
    assert 'total_nodes' in agent_data, "JSON missing 'total_nodes' key"

    golden_scores = compute_golden_scores(csv_path)

    # Sort golden scores descending
    sorted_golden = sorted(golden_scores.items(), key=lambda x: x[1], reverse=True)
    top_50_golden = sorted_golden[:50]
    truth_dict = {str(k): v for k, v in top_50_golden}

    agent_scores = []
    truth_scores = []

    for item in agent_data['results']:
        node = str(item['node_id'])
        if node in truth_dict:
            agent_scores.append(item['score'])
            truth_scores.append(truth_dict[node])
        else:
            # Penalize missing/incorrect nodes
            agent_scores.append(item['score'])
            truth_scores.append(0.0)

    # If agent returned fewer than 50 results, pad with 0s to match length if needed,
    # but the prompt says "for the 50 nodes present in the agent's output".
    # Wait, the prompt says "for the 50 nodes present in the agent's output compared to the golden standard scores for those exact nodes."
    # If the agent output is empty, it will fail.
    assert len(agent_scores) > 0, "Agent output contains no results"

    mse = np.mean((np.array(agent_scores) - np.array(truth_scores))**2)

    assert mse <= 1e-5, f"MSE {mse} is greater than threshold 1e-5"