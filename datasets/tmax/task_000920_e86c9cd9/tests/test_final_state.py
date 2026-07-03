# test_final_state.py
import os
import csv
import re

def test_venv_exists():
    assert os.path.isdir('/home/user/venv'), "Virtual environment at /home/user/venv does not exist."
    # Check for python executable in venv
    assert os.path.isfile('/home/user/venv/bin/python'), "Python executable not found in /home/user/venv/bin/."

def test_evaluate_script():
    script_path = '/home/user/evaluate.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert not re.search(r'\bpython\b', content, re.IGNORECASE), "evaluate.sh must not use Python."

def test_predictions_and_metrics():
    preds_path = '/home/user/predictions.csv'
    metrics_path = '/home/user/metrics.txt'

    assert os.path.isfile(preds_path), f"{preds_path} does not exist. Did you run the pipeline?"

    with open(preds_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['id', 'predicted_sentiment', 'true_sentiment'], "predictions.csv header is incorrect."

        correct = 0
        total = 0
        for row in reader:
            if not row:
                continue
            assert len(row) == 3, "predictions.csv must have exactly 3 columns."
            if row[1] == row[2]:
                correct += 1
            total += 1

    assert total == 200, f"Expected 200 test samples (20% of 1000), got {total}."

    expected_accuracy = correct / total

    assert os.path.isfile(metrics_path), f"{metrics_path} does not exist. Did you run evaluate.sh?"

    with open(metrics_path, 'r') as f:
        metrics_content = f.read().strip()

    match = re.match(r'^Accuracy:\s*([0-9]*\.?[0-9]+)$', metrics_content)
    assert match, f"{metrics_path} must contain exactly 'Accuracy: 0.XXXX'. Got: {metrics_content}"

    reported_accuracy = float(match.group(1))
    assert abs(reported_accuracy - expected_accuracy) < 1e-4, f"Reported accuracy {reported_accuracy} does not match calculated accuracy {expected_accuracy}."

def test_pipeline_code_fixed():
    pipeline_path = '/home/user/model_pipeline.py'
    assert os.path.isfile(pipeline_path), f"{pipeline_path} does not exist."

    with open(pipeline_path, 'r') as f:
        content = f.read()

    # Check that fit_transform is not called on the entire dataframe
    # A simple heuristic: ensure fit_transform is not called before train_test_split
    # But since we can't easily parse Python, let's just ensure it doesn't contain the exact leaky line
    assert "vectorizer.fit_transform(df['review_text'])" not in content, "The pipeline still contains the leaky code."