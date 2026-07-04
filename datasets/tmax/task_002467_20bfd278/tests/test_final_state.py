# test_final_state.py
import os
import stat
import re
import glob

def get_redacted_indices(text):
    return set(m.start() for m in re.finditer(r'\[REDACTED\]', text))

def evaluate(pred_path, truth_path):
    with open(pred_path, 'r', encoding='utf-8') as f: 
        pred = f.read()
    with open(truth_path, 'r', encoding='utf-8') as f: 
        truth = f.read()

    pred_idx = get_redacted_indices(pred)
    truth_idx = get_redacted_indices(truth)

    tp = len(pred_idx.intersection(truth_idx))
    fp = len(pred_idx - truth_idx)
    fn = len(truth_idx - pred_idx)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return f1

def test_redacted_logs_exist_and_permissions():
    pred_path = "/home/user/redacted_logs.txt"
    assert os.path.exists(pred_path), f"File not found: {pred_path}"

    st = os.stat(pred_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Expected permissions 0o600 for {pred_path}, but got {oct(perms)}"

def test_python_scripts_permissions():
    scripts = glob.glob("/home/user/*.py")
    for script in scripts:
        if os.path.basename(script) == "test_final_state.py":
            continue
        st = os.stat(script)
        perms = stat.S_IMODE(st.st_mode)
        assert perms == 0o600, f"Expected permissions 0o600 for script {script}, but got {oct(perms)}"

def test_f1_score():
    pred_path = "/home/user/redacted_logs.txt"
    truth_path = "/app/truth_redacted_logs.txt"

    assert os.path.exists(pred_path), f"Prediction file not found: {pred_path}"
    assert os.path.exists(truth_path), f"Truth file not found: {truth_path}"

    f1 = evaluate(pred_path, truth_path)
    assert f1 >= 0.99, f"F1 score {f1:.4f} is below the threshold of 0.99"