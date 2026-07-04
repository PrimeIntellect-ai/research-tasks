# test_final_state.py

import os
import csv
import subprocess
import sys

def test_clean_reviews_csv():
    """Test that clean_reviews.csv exists, retains the header, and only contains 'Verified' status."""
    clean_path = "/home/user/clean_reviews.csv"
    raw_path = "/home/user/raw_reviews.csv"

    assert os.path.exists(clean_path), f"File {clean_path} does not exist."
    assert os.path.isfile(clean_path), f"Path {clean_path} is not a file."

    with open(clean_path, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, f"File {clean_path} is empty."

        expected_header = ["ID", "Date", "Status", "Review_Text"]
        assert header == expected_header, f"Expected header {expected_header}, but got {header}."

        verified_count = 0
        for row_idx, row in enumerate(reader, start=2):
            assert len(row) == 4, f"Row {row_idx} does not have 4 columns."
            assert row[2] == "Verified", f"Row {row_idx} has Status '{row[2]}' instead of 'Verified'."
            verified_count += 1

    # Count expected verified rows from raw_reviews.csv
    expected_verified_count = 0
    if os.path.exists(raw_path):
        with open(raw_path, 'r', newline='') as f:
            raw_reader = csv.reader(f)
            next(raw_reader, None) # skip header
            for row in raw_reader:
                if len(row) >= 3 and row[2] == "Verified":
                    expected_verified_count += 1

    assert verified_count == expected_verified_count, (
        f"Expected {expected_verified_count} verified rows based on raw data, "
        f"but found {verified_count} in {clean_path}."
    )

def get_expected_id():
    """Run a subprocess to compute the expected ID using pandas and scikit-learn."""
    script = """
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

# Recreate clean_reviews.csv logic in memory from raw_reviews.csv
raw_df = pd.read_csv('/home/user/raw_reviews.csv')
clean_df = raw_df[raw_df['Status'] == 'Verified'].reset_index(drop=True)

tfidf = TfidfVectorizer(stop_words='english', max_features=200)
X_tfidf = tfidf.fit_transform(clean_df['Review_Text'])

svd = TruncatedSVD(n_components=5, random_state=42)
X_reduced = svd.fit_transform(X_tfidf)

kmeans = KMeans(n_clusters=4, n_init=10, random_state=42)
labels = kmeans.fit_predict(X_reduced)

cluster_0_indices = np.where(labels == 0)[0]
cluster_0_points = X_reduced[cluster_0_indices]
centroid_0 = kmeans.cluster_centers_[0].reshape(1, -1)

distances = euclidean_distances(cluster_0_points, centroid_0)
closest_idx_in_cluster = np.argmin(distances)
closest_original_idx = cluster_0_indices[closest_idx_in_cluster]

print(clean_df.iloc[closest_original_idx]['ID'])
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to compute expected ID. Stderr: {result.stderr}")
    return result.stdout.strip()

def test_representative_review_txt():
    """Test that representative_review.txt exists and contains the correct ID."""
    result_path = "/home/user/representative_review.txt"

    assert os.path.exists(result_path), f"File {result_path} does not exist."
    assert os.path.isfile(result_path), f"Path {result_path} is not a file."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"File {result_path} must contain ONLY a single integer ID. Got: '{content}'"

    expected_id = get_expected_id()
    assert content == expected_id, f"Expected representative ID {expected_id}, but got {content}."