# test_final_state.py
import json
import os
import pandas as pd
import numpy as np
import pytest
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge
from sklearn.metrics.pairwise import cosine_similarity

def test_recommendations_overlap():
    output_path = '/home/user/top_similar.json'
    assert os.path.exists(output_path), f"Expected output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        try:
            pred_top3 = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON.")

    # Golden logic to compute the expected top 3 recommendations
    df = pd.read_csv('/app/dataset.csv')
    features = [f'f{i+1}' for i in range(20)]

    X = df[features].values
    z_scores = np.abs((X - np.nanmean(X, axis=0)) / np.nanstd(X, axis=0))
    X[z_scores > 2.0] = np.nan

    imputer = IterativeImputer(estimator=BayesianRidge(), random_state=42, max_iter=20)
    X_imputed = imputer.fit_transform(X)

    sim = cosine_similarity(X_imputed)
    np.fill_diagonal(sim, -np.inf)

    golden_top3 = {}
    for i in range(50):
        golden_top3[str(i)] = np.argsort(sim[i])[::-1][:3].tolist()

    # Calculate overlap score
    overlap = 0
    for k, v in golden_top3.items():
        if k in pred_top3 and isinstance(pred_top3[k], list):
            overlap += len(set(v).intersection(set(pred_top3[k])))

    overlap_score = overlap / (50 * 3)

    assert overlap_score >= 0.9, f"Overlap score {overlap_score:.3f} is below the threshold of 0.9."