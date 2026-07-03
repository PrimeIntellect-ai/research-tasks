# test_final_state.py
import os
import csv
import math

def test_stat_result():
    stat_file = "/home/user/stat_result.txt"
    raw_data = "/home/user/raw_data.csv"

    assert os.path.exists(stat_file), f"File {stat_file} is missing."
    assert os.path.isfile(stat_file), f"Path {stat_file} is not a file."

    # Compute the expected result
    vals_A = []
    vals_B = []
    with open(raw_data, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            val = float(row['value'])
            if row['category'] == 'A':
                vals_A.append(val)
            elif row['category'] == 'B':
                vals_B.append(val)

    sum_A = math.fsum(vals_A)
    sum_B = math.fsum(vals_B)
    diff = sum_A - sum_B
    expected_str = f"{diff:.15f}"

    with open(stat_file, 'r') as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Expected {expected_str} in {stat_file}, but got {actual_str}"

def test_plot_png():
    plot_file = "/home/user/plot.png"
    assert os.path.exists(plot_file), f"File {plot_file} is missing."
    assert os.path.isfile(plot_file), f"Path {plot_file} is not a file."

    # Check if it is a valid PNG file by reading the magic number
    with open(plot_file, 'rb') as f:
        header = f.read(8)

    png_magic = b'\x89PNG\r\n\x1a\n'
    assert header == png_magic, f"File {plot_file} is not a valid PNG image."