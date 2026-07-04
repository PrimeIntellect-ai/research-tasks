# test_final_state.py
import os
import glob

def test_chunks_directory_exists():
    path = "/home/user/chunks"
    assert os.path.isdir(path), f"Directory {path} was not created."

def test_chunks_files_exist():
    path = "/home/user/chunks"
    assert os.path.isdir(path), f"Directory {path} was not created."
    files = glob.glob(os.path.join(path, "*.fa"))
    assert len(files) >= 6, f"Expected at least 6 .fa files in {path}, found {len(files)}."

def test_high_gc_anomalies_file_contents():
    path = "/home/user/high_gc_anomalies.txt"
    assert os.path.isfile(path), f"Output file {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["Seq2_High", "Seq4_High", "Seq5_Border"]

    assert lines == expected, f"File {path} does not contain the correct sorted sequence IDs. Expected: {expected}, Got: {lines}"