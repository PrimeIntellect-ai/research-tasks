# test_final_state.py

import os
import subprocess
import pytest

TOP_WORDS_PATH = "/home/user/data_pipeline/top_words.txt"
VERIFY_SCRIPT_PATH = "/home/user/data_pipeline/verify.sh"
PROCESS_SCRIPT_PATH = "/home/user/data_pipeline/process.sh"

EXPECTED_TOP_WORDS = """5 the
3 systematic
2 dog
2 enterprise
2 fox
"""

def test_top_words_exists_and_correct():
    assert os.path.isfile(TOP_WORDS_PATH), f"{TOP_WORDS_PATH} is missing."

    with open(TOP_WORDS_PATH, "r") as f:
        content = f.read()

    # Strip trailing whitespace/newlines from both for a fair comparison
    actual_lines = [line.strip() for line in content.strip().split("\n")]
    expected_lines = [line.strip() for line in EXPECTED_TOP_WORDS.strip().split("\n")]

    assert actual_lines == expected_lines, f"Contents of {TOP_WORDS_PATH} do not match the expected output. Got: {actual_lines}"

def test_verify_script_exists_and_executable():
    assert os.path.isfile(VERIFY_SCRIPT_PATH), f"{VERIFY_SCRIPT_PATH} is missing."
    # The task doesn't explicitly mandate chmod +x, but it's a script. We'll run it with bash just in case,
    # but let's check if it exists.

def test_verify_script_behavior():
    # First, run it with the correct top_words.txt
    result_correct = subprocess.run(["bash", VERIFY_SCRIPT_PATH], capture_output=True)
    assert result_correct.returncode == 0, f"{VERIFY_SCRIPT_PATH} should return exit code 0 when top_words.txt is correct."

    # Now, temporarily modify top_words.txt to test if verify.sh catches errors
    with open(TOP_WORDS_PATH, "r") as f:
        original_content = f.read()

    try:
        with open(TOP_WORDS_PATH, "w") as f:
            f.write("5 the\n3 systematic\n2 dog\n2 enterprise\n2 WRONGWORD\n")

        result_incorrect = subprocess.run(["bash", VERIFY_SCRIPT_PATH], capture_output=True)
        assert result_incorrect.returncode == 1, f"{VERIFY_SCRIPT_PATH} should return exit code 1 when top_words.txt is incorrect."

        # Test wrong number of lines
        with open(TOP_WORDS_PATH, "w") as f:
            f.write("5 the\n3 systematic\n2 dog\n2 enterprise\n")

        result_wrong_lines = subprocess.run(["bash", VERIFY_SCRIPT_PATH], capture_output=True)
        assert result_wrong_lines.returncode == 1, f"{VERIFY_SCRIPT_PATH} should return exit code 1 when top_words.txt has incorrect number of lines."

    finally:
        # Restore original content
        with open(TOP_WORDS_PATH, "w") as f:
            f.write(original_content)