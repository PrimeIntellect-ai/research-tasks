# test_final_state.py

import os
import csv
import subprocess

def compute_expected_variance():
    data_csv_path = "/home/user/data.csv"
    if not os.path.exists(data_csv_path):
        return None

    with open(data_csv_path, 'r') as f:
        reader = csv.reader(f)
        data = [int(row[0]) for row in reader if row]

    n = len(data)
    if n == 0:
        return 0.0

    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    return variance

def test_result_txt_exists_and_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected_variance = compute_expected_variance()
    assert expected_variance is not None, "data.csv is missing, cannot compute expected variance."

    expected_str = f"{expected_variance:.2f}"

    assert content == expected_str, f"Expected variance {expected_str} in result.txt, but got {content}."

def test_main_rs_streaming():
    main_rs_path = "/home/user/stats_service/src/main.rs"
    assert os.path.isfile(main_rs_path), f"File {main_rs_path} does not exist."

    with open(main_rs_path, 'r') as f:
        content = f.read()

    assert ".push(" not in content, "The code still contains '.push(', indicating it might not be fully streaming."
    assert "Vec::new()" not in content or "numbers" not in content, "The code still appears to allocate a Vec for all numbers."

def test_cargo_build_succeeds():
    project_dir = "/home/user/stats_service"
    assert os.path.isdir(project_dir), f"Directory {project_dir} does not exist."

    result = subprocess.run(
        ["cargo", "build"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"cargo build failed with error:\n{result.stderr}"