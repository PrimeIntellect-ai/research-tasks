# test_final_state.py
import os
import stat
import pytest

def compute_vcd(text):
    v = sum(1 for char in text if char.lower() in 'aeiou')
    c = sum(1 for char in text if char.isalpha() and char.lower() not in 'aeiou')
    d = sum(1 for char in text if char.isdigit())
    return v, c, d

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Pipeline script {script_path} is not executable."

def test_embeddings_csv():
    raw_path = "/home/user/data/raw.txt"
    csv_path = "/home/user/data/embeddings.csv"

    assert os.path.isfile(raw_path), f"Input file {raw_path} is missing."
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    with open(raw_path, "r") as f:
        lines = f.read().splitlines()

    expected_csv_lines = ["id,v,c,d"]
    for i, line in enumerate(lines):
        v, c, d = compute_vcd(line)
        expected_csv_lines.append(f"{i},{v},{c},{d}")

    with open(csv_path, "r") as f:
        actual_csv_lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert actual_csv_lines == expected_csv_lines, "The embeddings.csv does not match the expected output."

def test_predictions_txt():
    raw_path = "/home/user/data/raw.txt"
    txt_path = "/home/user/data/predictions.txt"

    assert os.path.isfile(raw_path), f"Input file {raw_path} is missing."
    assert os.path.isfile(txt_path), f"Output file {txt_path} is missing."

    with open(raw_path, "r") as f:
        lines = f.read().splitlines()

    expected_txt_lines = []
    for i, line in enumerate(lines):
        v, c, d = compute_vcd(line)
        score = (v * 1.5) + (c * -0.5) + (d * 2.0)
        expected_txt_lines.append(f"{i},{score:.1f}")

    with open(txt_path, "r") as f:
        actual_txt_lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert actual_txt_lines == expected_txt_lines, "The predictions.txt does not match the expected output."

def test_closest_txt():
    raw_path = "/home/user/data/raw.txt"
    txt_path = "/home/user/data/closest.txt"

    assert os.path.isfile(raw_path), f"Input file {raw_path} is missing."
    assert os.path.isfile(txt_path), f"Output file {txt_path} is missing."

    with open(raw_path, "r") as f:
        lines = f.read().splitlines()

    min_dist = float('inf')
    best_id = -1

    for i, line in enumerate(lines):
        v, c, d = compute_vcd(line)
        dist = (v - 5)**2 + (c - 10)**2 + (d - 3)**2
        if dist < min_dist:
            min_dist = dist
            best_id = i

    with open(txt_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == str(best_id), f"The closest.txt content should be '{best_id}', but got '{actual_content}'."