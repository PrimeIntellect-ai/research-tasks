# test_final_state.py
import os

def test_pipeline_script_exists():
    assert os.path.exists("/home/user/pipeline.sh"), "pipeline.sh is missing"

def test_c_program_exists():
    assert os.path.exists("/home/user/process.c"), "process.c is missing"

def test_pipeline_log_content():
    log_path = "/home/user/pipeline.log"
    assert os.path.exists(log_path), "pipeline.log is missing"

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read().strip().split()

    expected_words = ["Started", "Sorted", "Processed", "Done"]
    # Check if all expected words are in the log in the correct relative order
    # The log might have other words, but these must appear in order.
    idx = -1
    for word in expected_words:
        try:
            idx = content.index(word, idx + 1)
        except ValueError:
            assert False, f"Expected word '{word}' not found or not in correct order in pipeline.log"

def test_output_csv_content():
    output_path = "/home/user/output.csv"
    assert os.path.exists(output_path), "output.csv is missing"

    expected_lines = [
        "B***b,1,5.00",
        "A***e,6,10.25",
        "D***a,4,10.17",
        "E***e,2,25.17",
        "C***e,8,26.67"
    ]

    with open(output_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output.csv, got {len(lines)}"

    for i, (expected, actual) in enumerate(zip(expected_lines, lines)):
        assert actual == expected, f"Mismatch at line {i+1} of output.csv: expected '{expected}', got '{actual}'"