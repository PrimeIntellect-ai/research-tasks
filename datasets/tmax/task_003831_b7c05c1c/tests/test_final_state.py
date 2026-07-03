# test_final_state.py

import os
import csv

def test_dataset_csv_exists_and_valid():
    """Check if dataset.csv exists, has rows, and final t is close to 2.0."""
    csv_file = "/home/user/dataset.csv"
    assert os.path.isfile(csv_file), f"{csv_file} is missing."

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["t", "y"], "dataset.csv header should be 't,y'."

        rows = list(reader)
        assert len(rows) > 0, "dataset.csv is empty."

        last_t = float(rows[-1][0])
        assert abs(last_t - 2.0) < 1e-3, f"Integration did not reach t=2.0. Last t was {last_t}."

def test_plot_gp_exists():
    """Check if plot.gp exists and contains gnuplot commands."""
    gp_file = "/home/user/plot.gp"
    assert os.path.isfile(gp_file), f"{gp_file} is missing."

    with open(gp_file, 'r') as f:
        content = f.read().lower()
        assert "dataset.csv" in content, "plot.gp does not reference dataset.csv."
        assert "plot" in content, "plot.gp does not contain a plot command."
        assert "png" in content, "plot.gp does not set the terminal to png."

def test_plot_png_exists():
    """Check if plot.png exists and is a valid PNG file."""
    png_file = "/home/user/plot.png"
    assert os.path.isfile(png_file), f"{png_file} is missing."

    with open(png_file, 'rb') as f:
        header = f.read(8)
        assert header == b'\x89PNG\r\n\x1a\n', f"{png_file} is not a valid PNG file."

def test_final_y_txt():
    """Check if final_y.txt exists and contains the correct small value."""
    txt_file = "/home/user/final_y.txt"
    assert os.path.isfile(txt_file), f"{txt_file} is missing."

    with open(txt_file, 'r') as f:
        content = f.read().strip()

    try:
        final_y = float(content)
    except ValueError:
        assert False, f"{txt_file} does not contain a valid float."

    assert abs(final_y) < 1e-5, f"Final y value {final_y} is too large. Expected close to 0."

    # Verify it matches the last row of dataset.csv
    csv_file = "/home/user/dataset.csv"
    if os.path.isfile(csv_file):
        with open(csv_file, 'r') as f:
            rows = list(csv.reader(f))
            if len(rows) > 1:
                last_y_csv = float(rows[-1][1])
                assert abs(final_y - last_y_csv) < 1e-9, "final_y.txt does not match the last y value in dataset.csv."