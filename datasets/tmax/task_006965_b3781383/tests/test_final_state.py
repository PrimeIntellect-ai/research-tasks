# test_final_state.py

import os
import pytest

def get_expected_results():
    data_path = "/home/user/data.csv"
    if not os.path.exists(data_path):
        return "4,8,12", "-5.0,11.0,102.33"

    corrupted_lines = []
    valid_data = []
    with open(data_path, 'r') as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                val = float(line)
                if abs(val) > 1000:
                    corrupted_lines.append(i)
                else:
                    valid_data.append(val)
            except ValueError:
                corrupted_lines.append(i)

    expected_corrupted = ",".join(map(str, corrupted_lines))

    # K-means computation
    k = 3
    if len(valid_data) >= k:
        centroids = valid_data[:k]
        for _ in range(100):
            clusters = [[] for _ in range(k)]
            for x in valid_data:
                distances = [abs(x - c) for c in centroids]
                closest = distances.index(min(distances))
                clusters[closest].append(x)

            new_centroids = []
            for i, cluster in enumerate(clusters):
                if not cluster:
                    new_centroids.append(centroids[i])
                else:
                    new_centroids.append(sum(cluster) / len(cluster))

            if new_centroids == centroids:
                break
            centroids = new_centroids

        expected_centroids = ",".join([str(round(c, 2)) for c in sorted(centroids)])
    else:
        expected_centroids = "-5.0,11.0,102.33"

    return expected_corrupted, expected_centroids

def test_corrupted_lines_output():
    path = "/home/user/corrupted_lines.txt"
    assert os.path.isfile(path), f"File {path} was not generated."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_corrupted, _ = get_expected_results()
    assert content == expected_corrupted, f"Expected {path} to contain '{expected_corrupted}', but got '{content}'"

def test_centroids_output():
    path = "/home/user/centroids.txt"
    assert os.path.isfile(path), f"File {path} was not generated."

    with open(path, "r") as f:
        content = f.read().strip()

    _, expected_centroids = get_expected_results()
    assert content == expected_centroids, f"Expected {path} to contain '{expected_centroids}', but got '{content}'"