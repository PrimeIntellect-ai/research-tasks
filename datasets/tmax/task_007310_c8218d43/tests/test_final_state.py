# test_final_state.py
import os
import csv

def parse_train_data(filepath):
    valid_rows = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) != 7:
                continue
            try:
                id_val = int(row[0])
                label = int(row[1])
                if label not in (0, 1):
                    continue
                v = [float(x) for x in row[2:7]]
                valid_rows.append((id_val, label, v))
            except ValueError:
                continue
    return valid_rows

def parse_test_data(filepath):
    rows = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) != 6:
                continue
            try:
                id_val = int(row[0])
                v = [float(x) for x in row[1:6]]
                rows.append((id_val, v))
            except ValueError:
                continue
    return rows

def dist(v1, v2):
    return sum((a - b)**2 for a, b in zip(v1, v2))

def knn_predict(train_data, test_point, k):
    distances = []
    for row in train_data:
        d = dist(row[2], test_point)
        distances.append((d, row[0], row[1]))
    # Sort by distance, then by id to break ties
    distances.sort(key=lambda x: (x[0], x[1]))
    top_k = distances[:k]
    votes = [x[2] for x in top_k]
    count_1 = sum(votes)
    count_0 = k - count_1
    return 1 if count_1 > count_0 else 0

def get_expected_results():
    train_data = parse_train_data('/home/user/train.csv')
    test_data = parse_test_data('/home/user/test.csv')

    folds = {0: [], 1: [], 2: []}
    for i, row in enumerate(train_data):
        folds[i % 3].append(row)

    best_k = None
    best_acc = -1

    for k in [1, 3, 5, 7]:
        correct = 0
        total = 0
        for i in range(3):
            val_set = folds[i]
            train_set = folds[(i+1)%3] + folds[(i+2)%3]
            for val_row in val_set:
                pred = knn_predict(train_set, val_row[2], k)
                if pred == val_row[1]:
                    correct += 1
                total += 1
        acc = correct / total
        if acc > best_acc:
            best_acc = acc
            best_k = k

    predictions = []
    for test_row in test_data:
        pred = knn_predict(train_data, test_row[1], best_k)
        predictions.append((test_row[0], pred))

    return best_k, predictions

def test_best_k_file():
    best_k_path = '/home/user/best_k.txt'
    assert os.path.exists(best_k_path), f"File {best_k_path} is missing."

    with open(best_k_path, 'r') as f:
        content = f.read().strip()

    expected_k, _ = get_expected_results()

    assert content.isdigit(), f"Content of {best_k_path} is not an integer: '{content}'"
    assert int(content) == expected_k, f"Expected best k to be {expected_k}, but got {content}."

def test_predictions_file():
    preds_path = '/home/user/predictions.csv'
    assert os.path.exists(preds_path), f"File {preds_path} is missing."

    _, expected_preds = get_expected_results()
    expected_dict = dict(expected_preds)

    with open(preds_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['id', 'label'], f"Expected header ['id', 'label'], got {header}"

        actual_preds = {}
        for row in reader:
            assert len(row) == 2, f"Malformed row in predictions.csv: {row}"
            actual_preds[int(row[0])] = int(row[1])

    assert len(actual_preds) == len(expected_dict), f"Expected {len(expected_dict)} predictions, got {len(actual_preds)}"

    for test_id, expected_label in expected_dict.items():
        assert test_id in actual_preds, f"Prediction for id {test_id} is missing."
        assert actual_preds[test_id] == expected_label, f"Expected label {expected_label} for id {test_id}, got {actual_preds[test_id]}."