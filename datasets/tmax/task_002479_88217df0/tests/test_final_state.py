# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_recommendations_intersection():
    recommendations_file = '/home/user/recommendations.txt'
    dataset_file = '/app/items.csv'

    assert os.path.exists(recommendations_file), f"Recommendations file not found at {recommendations_file}"
    assert os.path.exists(dataset_file), f"Dataset file not found at {dataset_file}"

    # 1. Read dataset
    df = pd.read_csv(dataset_file)

    # 2. Impute means
    for col in ['f1', 'f2', 'f3', 'f4', 'f5']:
        mean_val = df[col].mean()
        df[col] = df[col].fillna(mean_val)

    # 3. Calculate distance
    target = np.array([12.5, 45.2, 8.9, 101.3, 55.0])
    def calc_dist(row):
        vec = np.array([row['f1'], row['f2'], row['f3'], row['f4'], row['f5']])
        return np.linalg.norm(vec - target)

    df['dist'] = df.apply(calc_dist, axis=1)

    # 4. Get true top 10
    true_top_10 = set(df.nsmallest(10, 'dist')['item_id'].astype(int).tolist())

    # 5. Read agent predictions
    try:
        with open(recommendations_file, 'r') as f:
            agent_preds = [int(line.strip()) for line in f if line.strip().isdigit()]
        agent_top_10 = set(agent_preds[:10])
    except Exception as e:
        pytest.fail(f"Failed to read or parse {recommendations_file}: {e}")

    # 6. Calculate intersection
    intersection = len(true_top_10.intersection(agent_top_10))

    assert intersection >= 9, f"Intersection metric is {intersection}, expected >= 9. True top 10: {true_top_10}, Agent top 10: {agent_top_10}"