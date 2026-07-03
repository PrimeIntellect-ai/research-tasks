# test_final_state.py
import os
import re
import math

def test_data_gen_executable():
    path = "/home/user/data_gen"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_dataset_csv():
    path = "/home/user/dataset.csv"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        lines = f.read().strip().split('\n')
    assert len(lines) == 102, f"Expected 102 lines in {path}, found {len(lines)}."
    assert lines[0] == "x,y", f"Expected header 'x,y' in {path}, found '{lines[0]}'."

def test_regression_txt():
    path = "/home/user/regression.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    m_match = re.search(r"m=([0-9\.\-]+)", content)
    c_match = re.search(r"c=([0-9\.\-]+)", content)

    assert m_match, f"Could not find 'm=<value>' in {path}."
    assert c_match, f"Could not find 'c=<value>' in {path}."

    m_val = float(m_match.group(1))
    c_val = float(c_match.group(1))

    # Compute expected values
    xs = []
    ys = []
    for i in range(101):
        x = i * 0.1
        y = x
        for _ in range(10):
            y = y - (y**3 + y - x) / (3 * y**2 + 1)
        xs.append(x)
        ys.append(y)

    n = len(xs)
    sum_x = sum(xs)
    sum_y = sum(ys)
    sum_xy = sum(x*y for x, y in zip(xs, ys))
    sum_xx = sum(x*x for x in xs)

    expected_m = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
    expected_c = (sum_y - expected_m * sum_x) / n

    assert math.isclose(m_val, expected_m, abs_tol=0.001), f"Expected m around {expected_m:.4f}, got {m_val}"
    assert math.isclose(c_val, expected_c, abs_tol=0.001), f"Expected c around {expected_c:.4f}, got {c_val}"

def test_plot_svg():
    path = "/home/user/plot.svg"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().lower()

    assert "<svg" in content, f"{path} does not contain '<svg' element."
    assert "<line" in content, f"{path} does not contain '<line' element."
    assert "<circle" in content, f"{path} does not contain '<circle' element."