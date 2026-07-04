# test_final_state.py

import os
import pytest

def test_corpus_exists_and_correct():
    """Check that corpus.txt exists and contains the exact 5 lines."""
    corpus_path = "/home/user/corpus.txt"
    assert os.path.exists(corpus_path), f"File {corpus_path} does not exist."

    expected_lines = [
        "Deploying a machine learning model to production is hard.",
        "Deep learning models require a lot of data.",
        "We are learning how to deploy deep neural networks.",
        "The deployment of a deep learning model is a critical step.",
        "Data science involves analyzing data to find patterns."
    ]

    with open(corpus_path, "r") as f:
        actual_lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {corpus_path} do not match the expected 5 lines."

def test_script_exists():
    """Check that the bash script exists."""
    script_path = "/home/user/extract_similar.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

def test_top_matches_exists_and_correct():
    """Check that top_matches.txt exists and contains the correct sorted output."""
    matches_path = "/home/user/top_matches.txt"
    assert os.path.exists(matches_path), f"File {matches_path} does not exist."

    expected_lines = [
        "The deployment of a deep learning model is a critical step.",
        "Deep learning models require a lot of data.",
        "Deploying a machine learning model to production is hard."
    ]

    with open(matches_path, "r") as f:
        actual_lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {matches_path} do not match the expected top 3 matches."