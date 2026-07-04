# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_metrics_file_exists_and_correct():
    output_file = "/home/user/output/metrics.txt"
    assert os.path.exists(output_file), f"Output file does not exist: {output_file}"
    assert os.path.isfile(output_file), f"Path is not a file: {output_file}"

    with open(output_file, 'r') as f:
        content = f.read().strip()

    assert content, "The metrics.txt file is empty."

    try:
        user_val = float(content)
    except ValueError:
        pytest.fail(f"The content of metrics.txt is not a valid float: {content}")

    # Recompute the expected value using a subprocess to avoid importing third-party libs directly in the test
    golden_script = """
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('/home/user/data/articles.csv')
text_train, text_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(max_features=100)
X_train = vectorizer.fit_transform(text_train)
X_test = vectorizer.transform(text_test)

sim = cosine_similarity(X_test, X_train)
max_sims = sim.max(axis=1)
avg_max_sim = max_sims.mean()

print(f"{avg_max_sim:.4f}")
"""
    result = subprocess.run(
        [sys.executable, "-c", golden_script],
        capture_output=True,
        text=True,
        check=True
    )

    expected_val_str = result.stdout.strip()
    expected_val = float(expected_val_str)

    assert abs(user_val - expected_val) < 1e-4, (
        f"The calculated mean maximum similarity is incorrect. "
        f"Expected approximately {expected_val:.4f}, but got {user_val:.4f}. "
        f"Make sure the data leakage bug is fixed correctly."
    )