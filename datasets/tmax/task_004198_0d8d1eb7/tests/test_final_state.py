# test_final_state.py

import os
import math
import csv

def get_expected_best_model():
    """
    Computes the expected best alpha and its average validation accuracy.
    Since each fold has exactly 20 items, the average cross-validation accuracy
    is mathematically equivalent to the accuracy on the entire dataset.
    """
    csv_path = "/home/user/embeddings.csv"
    if not os.path.exists(csv_path):
        return None, None

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    alphas = [0.1, 0.3, 0.5, 0.7, 0.9]
    best_alpha = None
    best_acc = -1.0

    for alpha in alphas:
        correct = 0
        for row in rows:
            x1, x2, x3 = float(row[1]), float(row[2]), float(row[3])
            label = int(row[4])

            dist = math.sqrt((x1 - 1.0)**2 + (x2 - 1.0)**2 + (x3 - 1.0)**2)
            score = math.exp(-dist) * alpha
            pred = 1 if score > 0.1 else 0

            if pred == label:
                correct += 1

        # Since there are 5 folds of 20 items each, the average accuracy is simply total_correct / 100
        acc = correct / 100.0

        if acc > best_acc:
            best_acc = acc
            best_alpha = alpha
        elif acc == best_acc:
            if best_alpha is None or alpha < best_alpha:
                best_alpha = alpha

    return best_alpha, best_acc

def test_model_c_exists():
    """Test that the C implementation file exists."""
    file_path = "/home/user/model.c"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_tune_sh_exists():
    """Test that the shell script exists."""
    file_path = "/home/user/tune.sh"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_best_model_txt():
    """Test that best_model.txt contains the correct output."""
    file_path = "/home/user/best_model.txt"
    assert os.path.exists(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    best_alpha, best_acc = get_expected_best_model()
    assert best_alpha is not None, "Could not compute expected result because embeddings.csv is missing."

    # The expected output format is best_alpha,best_acc (accuracy to 2 decimal places)
    # E.g., "0.5,0.82"
    # Depending on how the student formatted alpha, it could be "0.5" or "0.50". 
    # We will parse the student's output to be robust.

    parts = content.split(",")
    assert len(parts) == 2, f"Expected format 'alpha,accuracy' in {file_path}, but got '{content}'"

    try:
        student_alpha = float(parts[0].strip())
        student_acc = float(parts[1].strip())
    except ValueError:
        assert False, f"Could not parse float values from {file_path} content: '{content}'"

    # Check alpha
    assert math.isclose(student_alpha, best_alpha, rel_tol=1e-5), \
        f"Expected best alpha to be {best_alpha}, but got {student_alpha}."

    # Check accuracy (rounded to 2 decimal places)
    expected_acc_rounded = round(best_acc, 2)
    assert math.isclose(student_acc, expected_acc_rounded, rel_tol=1e-5) or math.isclose(student_acc, best_acc, rel_tol=1e-5), \
        f"Expected accuracy to be {expected_acc_rounded}, but got {student_acc}."