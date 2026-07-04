# test_final_state.py

import os
import pytest
import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def test_ingest_script_exists():
    path = "/home/user/ingest_data.py"
    assert os.path.isfile(path), f"Ingest script missing at {path}"

def test_nginx_routing_and_recall_metric():
    csv_path = "/home/user/data/training_data.csv"
    assert os.path.isfile(csv_path), f"Data file missing at {csv_path}"

    # Read the dataset
    df = pd.read_csv(csv_path)
    assert 'id' in df.columns and 'description' in df.columns, "CSV must contain 'id' and 'description' columns"

    # Compute ground truth TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['description'].fillna(''))

    # Select 20 test queries from the dataset
    np.random.seed(42)
    sample_indices = np.random.choice(len(df), size=min(20, len(df)), replace=False)
    queries = df.iloc[sample_indices]['description'].tolist()

    recalls = []
    for idx, query in zip(sample_indices, queries):
        # Ground truth top 5
        q_vec = vectorizer.transform([query])
        sims = cosine_similarity(q_vec, tfidf_matrix).flatten()
        top5_idx = sims.argsort()[-5:][::-1]
        gt_ids = set(df.iloc[top5_idx]['id'].values)

        # Query the API via Nginx
        try:
            resp = requests.get("http://localhost:8080/api/search", params={'query': query}, timeout=5)
            assert resp.status_code == 200, f"API returned status {resp.status_code} for /api/search"
            data = resp.json()
        except Exception as e:
            pytest.fail(f"Failed to query the search endpoint: {e}")

        # Extract IDs from the response
        pred_ids = []
        if isinstance(data, list):
            pred_ids = data
        elif isinstance(data, dict):
            for key in ['ids', 'results', 'data']:
                if key in data:
                    pred_data = data[key]
                    if pred_data and isinstance(pred_data[0], dict) and 'id' in pred_data[0]:
                        pred_ids = [item['id'] for item in pred_data]
                    else:
                        pred_ids = pred_data
                    break

        if not pred_ids:
            pytest.fail(f"Could not extract IDs from API response: {data}")

        pred_ids_set = set(pred_ids[:5])

        # Calculate Recall@5
        recall = len(gt_ids.intersection(pred_ids_set)) / 5.0
        recalls.append(recall)

    avg_recall = np.mean(recalls)
    assert avg_recall >= 0.85, f"Average Recall@5 is {avg_recall:.2f}, which is below the threshold of 0.85"