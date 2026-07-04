# test_final_state.py
import os

def test_cpp_file_exists():
    file_path = "/home/user/predictor.cpp"
    assert os.path.isfile(file_path), f"C++ source file missing: {file_path}"

def test_predictions_file_exists_and_correct():
    pred_path = "/home/user/predictions.txt"
    assert os.path.isfile(pred_path), f"Predictions file missing: {pred_path}. Did the C++ program run and generate it?"

    with open(pred_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 non-empty lines in predictions.txt, found {len(lines)}"

    assert lines[0] == "Best K: 2", f"Expected first line to be 'Best K: 2', got '{lines[0]}'"
    assert lines[1] == "5,80.50", f"Expected second line to be '5,80.50', got '{lines[1]}'"
    assert lines[2] == "7,80.00", f"Expected third line to be '7,80.00', got '{lines[2]}'"