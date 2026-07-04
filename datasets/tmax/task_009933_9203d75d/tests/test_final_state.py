# test_final_state.py
import os
import csv

def test_predictor_go_exists():
    path = "/home/user/predictor.go"
    assert os.path.isfile(path), f"Expected Go source file {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content.startswith("package main") or "func main()" in content, f"File {path} does not appear to be a valid Go program."

def test_predictions_csv_correct():
    path = "/home/user/predictions.csv"
    assert os.path.isfile(path), f"Expected predictions file {path} does not exist."

    expected_rows = {
        "Q1": "90.00",
        "Q2": "25.17",
        "Q3": "105.17",
        "Q4": "25.17"
    }

    with open(path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["QueryID", "Predicted_Duration"], f"Incorrect header in {path}. Expected ['QueryID', 'Predicted_Duration'], got {header}."

        actual_rows = {}
        for row in reader:
            assert len(row) == 2, f"Invalid row length in {path}: {row}"
            actual_rows[row[0]] = row[1]

    assert actual_rows == expected_rows, f"Predictions in {path} do not match expected values. Expected {expected_rows}, got {actual_rows}."

def test_benchmark_txt_valid():
    path = "/home/user/benchmark.txt"
    assert os.path.isfile(path), f"Expected benchmark file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content, f"File {path} is empty."

    try:
        val = int(content)
    except ValueError:
        pytest.fail(f"File {path} does not contain a valid integer. Content: '{content}'")

    assert val >= 0, f"Benchmark time in {path} should be a non-negative integer."