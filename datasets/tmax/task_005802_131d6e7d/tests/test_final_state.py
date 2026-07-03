# test_final_state.py
import os
import csv

def test_summary_csv():
    path = "/home/user/summary.csv"
    assert os.path.isfile(path), f"File {path} is missing. The script did not generate it."

    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"File {path} is empty."

    header = rows[0]
    assert header == ["architecture", "inference_ms"], f"Header in {path} is incorrect. Expected ['architecture', 'inference_ms'], got {header}"

    expected_data = {
        "cnn": 13.4,
        "rnn": 25.1,
        "transformer": 47.0
    }

    actual_data = {}
    for row in rows[1:]:
        assert len(row) == 2, f"Row {row} does not have exactly 2 columns."
        arch, val = row
        try:
            actual_data[arch] = float(val)
        except ValueError:
            assert False, f"Could not parse '{val}' as float in row {row}."

    assert len(actual_data) == 3, f"Expected 3 rows of data, got {len(actual_data)}."

    for arch, expected_val in expected_data.items():
        assert arch in actual_data, f"Architecture '{arch}' is missing from summary.csv."
        assert abs(actual_data[arch] - expected_val) < 1e-5, f"Expected {expected_val} for {arch}, got {actual_data[arch]}."

def test_benchmark_plot_png():
    path = "/home/user/benchmark_plot.png"
    assert os.path.isfile(path), f"File {path} is missing. The script did not generate it."

    file_size = os.path.getsize(path)
    assert file_size > 5000, f"File {path} is suspiciously small ({file_size} bytes), indicating an empty or invalid plot."

    with open(path, "rb") as f:
        magic_bytes = f.read(8)

    expected_magic = b"\x89PNG\r\n\x1a\n"
    assert magic_bytes == expected_magic, f"File {path} is not a valid PNG image. Magic bytes mismatch."