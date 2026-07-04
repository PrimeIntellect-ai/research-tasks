# test_final_state.py
import os

def test_results_file():
    results_path = '/home/user/results.txt'
    assert os.path.isfile(results_path), f"{results_path} does not exist."

    with open(results_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {results_path}, found {len(lines)}."
    assert lines[0] == "Accuracy: 0.8800", f"Line 1 incorrect. Expected 'Accuracy: 0.8800', got '{lines[0]}'"
    assert lines[1] == "Class 1 Prior: 0.3062", f"Line 2 incorrect. Expected 'Class 1 Prior: 0.3062', got '{lines[1]}'"

def test_pipeline_script_fixed():
    script_path = '/home/user/pipeline.py'
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    with open(script_path, 'r') as f:
        code = f.read()

    # Check that train_test_split appears before fit_transform
    tts_idx = code.find('train_test_split(')
    assert tts_idx != -1, "train_test_split() not found in pipeline.py"

    fit_idx = code.find('fit_transform(')
    assert fit_idx != -1, "fit_transform() not found in pipeline.py"

    assert tts_idx < fit_idx, "Data leakage bug not fixed: train_test_split must be called before fit_transform."