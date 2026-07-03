# test_final_state.py

import os
import pytest

TRUTH = "1010101110001100101011110000111100110101010001110010101011110000111100110101010001110010101011110000"
OUTPUT_PATH = "/home/user/output.txt"

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_PATH), f"Output file is missing at {OUTPUT_PATH}. Did you run the extraction and save the output?"

def test_output_file_accuracy():
    with open(OUTPUT_PATH, "r") as f:
        output = f.read().strip()

    assert output, "Output file is empty."
    assert len(output) == len(TRUTH), f"Output length is {len(output)}, but expected exactly {len(TRUTH)} bits."

    matches = sum(1 for a, b in zip(TRUTH, output) if a == b)
    accuracy = matches / len(TRUTH)

    assert accuracy >= 0.95, f"Accuracy is {accuracy:.4f} (Threshold: >= 0.95). The extracted bits do not match the ground truth closely enough."

def test_output_contains_only_binary():
    with open(OUTPUT_PATH, "r") as f:
        output = f.read().strip()

    invalid_chars = set(output) - {'0', '1'}
    assert not invalid_chars, f"Output contains invalid characters: {invalid_chars}. It should only contain '0' and '1'."