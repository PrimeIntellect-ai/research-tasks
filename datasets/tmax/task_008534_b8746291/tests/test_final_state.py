# test_final_state.py
import os
import csv
import math

def test_fixed_accuracy_file():
    accuracy_file = "/home/user/fixed_accuracy.txt"
    embeddings_file = "/home/user/embeddings.csv"

    assert os.path.isfile(accuracy_file), f"{accuracy_file} is missing. Did you save the accuracy?"
    assert os.path.isfile(embeddings_file), f"{embeddings_file} is missing."

    # Read the data to compute the expected accuracy dynamically
    data = []
    with open(embeddings_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([float(row[0]), float(row[1]), int(row[2])])

    assert len(data) == 100, "Expected exactly 100 rows in embeddings.csv"

    # Split data: 80 train, 20 test
    train = data[:80]
    test = data[80:]

    # Compute means and stds ONLY on train data
    num_features = 2
    means = [0.0] * num_features
    for row in train:
        for i in range(num_features):
            means[i] += row[i]
    for i in range(num_features):
        means[i] /= len(train)

    stds = [0.0] * num_features
    for row in train:
        for i in range(num_features):
            stds[i] += (row[i] - means[i]) ** 2
    for i in range(num_features):
        stds[i] = math.sqrt(stds[i] / len(train))

    # Normalize train and test data
    def normalize(dataset):
        norm_data = []
        for row in dataset:
            norm_row = []
            for i in range(num_features):
                val = (row[i] - means[i]) / stds[i] if stds[i] != 0 else 0.0
                norm_row.append(val)
            norm_row.append(row[2]) # Append label
            norm_data.append(norm_row)
        return norm_data

    norm_train = normalize(train)
    norm_test = normalize(test)

    # Train Nearest Centroid
    centroids = {}
    counts = {}
    for row in norm_train:
        lbl = row[2]
        if lbl not in centroids:
            centroids[lbl] = [0.0] * num_features
            counts[lbl] = 0
        for i in range(num_features):
            centroids[lbl][i] += row[i]
        counts[lbl] += 1

    for lbl in centroids:
        for i in range(num_features):
            centroids[lbl][i] /= counts[lbl]

    # Evaluate
    correct = 0
    for row in norm_test:
        best_lbl = -1
        min_dist = float('inf')
        for lbl, centroid in centroids.items():
            dist = 0.0
            for i in range(num_features):
                dist += (row[i] - centroid[i]) ** 2
            if dist < min_dist:
                min_dist = dist
                best_lbl = lbl
        if best_lbl == row[2]:
            correct += 1

    expected_accuracy = correct / len(test)

    # Check the student's output
    with open(accuracy_file, "r") as f:
        content = f.read().strip()

    try:
        actual_accuracy = float(content)
    except ValueError:
        assert False, f"File {accuracy_file} does not contain a valid decimal number. Content found: '{content}'"

    assert math.isclose(actual_accuracy, expected_accuracy, rel_tol=1e-4, abs_tol=1e-4), \
        f"Incorrect accuracy. Expected {expected_accuracy:.6f}, got {actual_accuracy:.6f}. Ensure data leakage is fixed properly."