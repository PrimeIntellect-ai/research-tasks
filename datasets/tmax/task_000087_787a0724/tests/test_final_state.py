# test_final_state.py
import os

def test_hyperparameter_tuning_result():
    dataset_path = "/home/user/dataset.csv"
    assert os.path.exists(dataset_path), f"Dataset file {dataset_path} is missing."

    with open(dataset_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 100, f"Expected 100 lines in {dataset_path}, found {len(lines)}."

    y = []
    texts = []
    for i, line in enumerate(lines):
        parts = line.strip().split(',', 1)
        assert len(parts) == 2, f"Line {i} is malformed."
        y.append(int(parts[0]))
        texts.append(parts[1].split(' '))

    best_acc = -1
    best_M = None
    best_T = None

    # Iterate in ascending order so the first max accuracy encountered 
    # automatically satisfies the "smallest M, then smallest T" tie-breaking rule.
    for M in [2, 3, 4, 5]:
        for T in [1, 2, 3]:
            correct = 0
            for label, tokens in zip(y, texts):
                count = sum(1 for token in tokens if len(token) > M)
                pred = 1 if count >= T else 0
                if pred == label:
                    correct += 1

            acc = correct / len(y)

            if acc > best_acc:
                best_acc = acc
                best_M = M
                best_T = T

    expected_result = f"{best_M},{best_T}"

    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"Result file {result_path} was not created."

    with open(result_path, 'r') as f:
        actual_result = f.read().strip()

    assert actual_result == expected_result, (
        f"Incorrect result in {result_path}. "
        f"Expected '{expected_result}' (M={best_M}, T={best_T} with accuracy {best_acc}), "
        f"but got '{actual_result}'."
    )