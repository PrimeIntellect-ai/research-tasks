# test_final_state.py

import os
import pytest
import pandas as pd
import numpy as np

def test_tiny_ann_fixed():
    path = "/app/tiny_ann/setup.py"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "import setuptools" in content, f"File {path} does not contain the fixed 'import setuptools'."
    assert "import setuptool\n" not in content and "import setuptool " not in content, \
        f"File {path} still contains the deliberate typo 'import setuptool'."

def test_tiny_ann_installed():
    try:
        import tiny_ann
        from tiny_ann import TinyIndex
    except ImportError as e:
        pytest.fail(f"tiny_ann package is not installed correctly or TinyIndex cannot be imported: {e}")

def test_recommendations_csv_exists_and_format():
    path = "/home/user/recommendations.csv"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    df = pd.read_csv(path)
    assert 'query_id' in df.columns, f"Column 'query_id' missing from {path}"
    assert 'recommended_item_ids' in df.columns, f"Column 'recommended_item_ids' missing from {path}"

def test_recall_metric():
    agent_path = "/home/user/recommendations.csv"
    golden_path = "/home/user/data/golden_recommendations.csv"

    assert os.path.isfile(agent_path), f"Agent recommendations file {agent_path} not found."
    assert os.path.isfile(golden_path), f"Golden recommendations file {golden_path} not found."

    agent_df = pd.read_csv(agent_path)
    golden_df = pd.read_csv(golden_path)

    merged = pd.merge(agent_df, golden_df, on="query_id", suffixes=('_agent', '_gold'))
    assert len(merged) > 0, "No matching query_ids found between agent and golden recommendations."

    recalls = []
    for _, row in merged.iterrows():
        agent_recs = set(str(row['recommended_item_ids_agent']).split())
        gold_recs = set(str(row['recommended_item_ids_gold']).split())

        # Calculate recall
        recall = len(agent_recs.intersection(gold_recs)) / 5.0
        recalls.append(recall)

    mean_recall = np.mean(recalls)
    assert mean_recall >= 0.85, f"Mean Recall@5 is {mean_recall:.4f}, which is below the threshold of 0.85"