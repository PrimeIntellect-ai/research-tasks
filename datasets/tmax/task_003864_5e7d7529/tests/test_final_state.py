# test_final_state.py

import json
import os
import sys

def test_metrics_json_exists():
    metrics_path = '/home/user/metrics.json'
    assert os.path.isfile(metrics_path), f"File {metrics_path} does not exist. The script did not generate the metrics output."

def test_metrics_json_contents():
    metrics_path = '/home/user/metrics.json'
    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            raise AssertionError("metrics.json is not a valid JSON file.")

    expected_keys = {"test_accuracy", "avg_inference_ms", "pipeline_steps"}
    missing_keys = expected_keys - set(metrics.keys())
    assert not missing_keys, f"metrics.json is missing required keys: {missing_keys}"

    assert isinstance(metrics["test_accuracy"], (int, float)), "test_accuracy must be a float"
    assert isinstance(metrics["avg_inference_ms"], (int, float)), "avg_inference_ms must be a float"
    assert isinstance(metrics["pipeline_steps"], list), "pipeline_steps must be a list of strings"
    assert all(isinstance(step, str) for step in metrics["pipeline_steps"]), "pipeline_steps must contain only strings"
    assert len(metrics["pipeline_steps"]) == 2, "pipeline_steps should have exactly 2 steps (vectorizer and classifier)"
    assert metrics["avg_inference_ms"] > 0, "avg_inference_ms must be greater than 0"

def test_accuracy_is_correct_no_data_leak():
    try:
        import pandas as pd
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        from sklearn.metrics import accuracy_score
    except ImportError as e:
        raise AssertionError(f"Required package missing: {e}")

    data_path = '/home/user/data.csv'
    assert os.path.isfile(data_path), f"Dataset {data_path} is missing."

    df = pd.read_csv(data_path)
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['label'], test_size=0.2, random_state=42
    )

    pipe = Pipeline([
        ('vec', TfidfVectorizer()),
        ('clf', LogisticRegression(random_state=42))
    ])
    pipe.fit(X_train, y_train)
    true_acc = accuracy_score(y_test, pipe.predict(X_test))

    metrics_path = '/home/user/metrics.json'
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)

    actual_acc = metrics["test_accuracy"]
    assert abs(actual_acc - true_acc) < 1e-4, (
        f"Accuracy mismatch. Expected {true_acc}, got {actual_acc}. "
        "Make sure the data leak is fixed (Pipeline is used), and random_state=42 is set for both split and LogisticRegression."
    )

def test_train_model_script_refactored():
    script_path = '/home/user/train_model.py'
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "Pipeline" in content, "The script does not seem to use sklearn.pipeline.Pipeline."
    assert "metrics.json" in content, "The script does not seem to save outputs to metrics.json."