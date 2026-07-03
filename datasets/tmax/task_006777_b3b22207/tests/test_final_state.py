# test_final_state.py

import os
import json
import pytest

def test_cleaned_waves_csv():
    path = "/home/user/cleaned_waves.csv"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, f"File {path} is empty."
    # The header is 1 line, plus 997 data rows = 998 lines
    assert len(lines) == 998, f"Expected exactly 998 lines (header + 997 rows) in {path}, but found {len(lines)}."

def test_benchmark_txt():
    path = "/home/user/benchmark.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {path} could not be parsed as a float. Content: '{content}'")

    assert val > 0.0, f"Benchmark time in {path} should be a positive float, got {val}."

def test_accuracy_json():
    path = "/home/user/accuracy.json"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "accurate" in data, f"'accurate' key missing in {path}."
    assert "parseval_diff" in data, f"'parseval_diff' key missing in {path}."

    assert data["accurate"] is True, f"Expected 'accurate' to be True, got {data['accurate']}."
    assert isinstance(data["parseval_diff"], (float, int)), f"'parseval_diff' should be a number."
    assert data["parseval_diff"] < 1e-5, f"Expected 'parseval_diff' to be < 1e-5, got {data['parseval_diff']}."

def test_spectrum_png():
    path = "/home/user/spectrum.png"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'rb') as f:
        header = f.read(8)

    assert header == b'\x89PNG\r\n\x1a\n', f"File {path} is not a valid PNG image."

    size = os.path.getsize(path)
    assert size > 3000, f"File {path} is suspiciously small ({size} bytes), likely a blank or broken plot."