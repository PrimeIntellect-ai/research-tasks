# test_final_state.py
import os
import joblib
import random
import pytest

def test_plot_results():
    path = '/home/user/cv_results.png'
    assert os.path.isfile(path), f"File {path} is missing. Did you fix and run plot_results.py?"
    assert os.path.getsize(path) > 0, f"File {path} is empty."

def test_model_accuracy():
    model_path = '/home/user/best_model.pkl'
    assert os.path.isfile(model_path), f"Model file {model_path} is missing."

    try:
        model = joblib.load(model_path)
    except Exception as e:
        pytest.fail(f"Failed to load model from {model_path}: {e}")

    positive_words = ["good", "great", "excellent", "amazing", "wonderful", "fantastic", "superb"]
    negative_words = ["bad", "terrible", "awful", "horrible", "poor", "disgusting", "useless"]

    random.seed(99)
    test_texts = []
    test_labels = []
    for _ in range(200):
        if random.random() > 0.5:
            text = f"I think it is {random.choice(positive_words)}."
            test_labels.append(1)
        else:
            text = f"I think it is {random.choice(negative_words)}."
            test_labels.append(0)

    try:
        preds = model.predict(test_texts)
    except Exception as e:
        pytest.fail(f"Model prediction failed: {e}")

    acc = sum(p == l for p, l in zip(preds, test_labels)) / len(test_labels)

    assert acc >= 0.85, f"Model accuracy {acc} is below the threshold of 0.85."