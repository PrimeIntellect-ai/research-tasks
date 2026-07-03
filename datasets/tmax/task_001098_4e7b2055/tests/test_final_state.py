# test_final_state.py

import os
import numpy as np
import pytest
from sklearn.cluster import KMeans

def test_centroids_mse():
    output_file = "/home/user/centroids.txt"
    dataset_file = "/app/forensic_logs.txt"

    assert os.path.isfile(output_file), f"Output file {output_file} is missing."
    assert os.path.isfile(dataset_file), f"Dataset file {dataset_file} is missing."

    # Load user centroids
    try:
        user_centroids = np.loadtxt(output_file, delimiter=',')
    except Exception as e:
        pytest.fail(f"Failed to parse {output_file} as comma-separated floats: {e}")

    assert user_centroids.shape[0] == 5, f"Expected exactly 5 centroids, got {user_centroids.shape[0]}"

    # Load dataset to compute ground truth
    try:
        # Try comma separated first, fallback to whitespace
        try:
            X = np.loadtxt(dataset_file, delimiter=',')
        except ValueError:
            X = np.loadtxt(dataset_file)
    except Exception as e:
        pytest.fail(f"Failed to load dataset {dataset_file}: {e}")

    # Compute reference centroids using sklearn
    kmeans = KMeans(n_clusters=5, n_init=10, random_state=42)
    kmeans.fit(X)
    ref_centroids = kmeans.cluster_centers_

    # Ensure dimensions match
    assert user_centroids.shape[1] == ref_centroids.shape[1], \
        f"Dimension mismatch: user centroids have {user_centroids.shape[1]} dims, expected {ref_centroids.shape[1]}"

    # Sort centroids lexically to align them
    def sort_centroids(c):
        # Lexsort sorts by the last row first, so we reverse the transposed array
        return c[np.lexsort(c.T[::-1])]

    user_sorted = sort_centroids(user_centroids)
    ref_sorted = sort_centroids(ref_centroids)

    # Compute Mean Squared Error
    mse = np.mean((user_sorted - ref_sorted) ** 2)

    threshold = 0.01
    assert mse <= threshold, f"MSE {mse:.6f} exceeds threshold {threshold}. The centroids do not match the expected clusters."