# test_final_state.py

import os
import pytest

OUTPUT_TXT = "/home/user/pipeline/output.txt"

def test_output_file_exists():
    """Verify that the output.txt file has been created."""
    assert os.path.isfile(OUTPUT_TXT), f"File {OUTPUT_TXT} does not exist. Did you run the processor?"

def test_output_file_content():
    """Verify that the processor generated the correct output."""
    assert os.path.isfile(OUTPUT_TXT), f"File {OUTPUT_TXT} does not exist."
    with open(OUTPUT_TXT, "r") as f:
        content = f.read().strip()

    expected = "PROCESSED: SECRET DEBUGGING PHRASE"
    assert content == expected, f"Content of {OUTPUT_TXT} is incorrect. Expected: '{expected}', but got: '{content}'"