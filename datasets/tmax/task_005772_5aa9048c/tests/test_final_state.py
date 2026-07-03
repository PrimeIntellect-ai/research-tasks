# test_final_state.py
import os
import json
import pytest

def test_training_data_csv():
    file_path = "/home/user/training_data.csv"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 6, f"Expected 6 lines in {file_path} (header + 5 rows), got {len(lines)}"

    header = lines[0]
    assert header == "user_id,age,event_count,avg_latency", f"Incorrect header in {file_path}"

    expected_rows = [
        "1,25,2,125.0",
        "2,30,1,200.0",
        "3,22,1,50.0",
        "4,35,2,305.0",
        "5,28,2,125.0"
    ]

    # Check if rows match exactly
    for i, expected in enumerate(expected_rows):
        # Allow slight formatting variations for floats (e.g., 125 vs 125.0)
        actual = lines[i+1].split(",")
        exp = expected.split(",")

        assert actual[0] == exp[0], f"Row {i+1} user_id mismatch: expected {exp[0]}, got {actual[0]}"
        assert actual[1] == exp[1], f"Row {i+1} age mismatch: expected {exp[1]}, got {actual[1]}"
        assert actual[2] == exp[2], f"Row {i+1} event_count mismatch: expected {exp[2]}, got {actual[2]}"
        assert float(actual[3]) == float(exp[3]), f"Row {i+1} avg_latency mismatch: expected {exp[3]}, got {actual[3]}"

def test_report_json():
    file_path = "/home/user/report.json"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not valid JSON.")

    assert "row_count" in data, f"Missing 'row_count' in {file_path}"
    assert data["row_count"] == 5, f"Expected row_count to be 5, got {data['row_count']}"

    assert "total_inference_time_seconds" in data, f"Missing 'total_inference_time_seconds' in {file_path}"
    assert isinstance(data["total_inference_time_seconds"], (int, float)), "total_inference_time_seconds must be a number"
    assert data["total_inference_time_seconds"] > 0, "total_inference_time_seconds must be greater than 0"

def test_plot_png():
    file_path = "/home/user/plot.png"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    size = os.path.getsize(file_path)
    assert size > 0, f"{file_path} is empty."

    with open(file_path, "rb") as f:
        header = f.read(8)

    # PNG magic bytes
    expected_magic = b'\x89PNG\r\n\x1a\n'
    assert header == expected_magic, f"{file_path} is not a valid PNG file (invalid magic bytes)."