# test_final_state.py

import os
import re
import difflib

def test_duplicates_log_exists():
    assert os.path.isfile("/home/user/duplicates.log"), "/home/user/duplicates.log does not exist. Did you run your script and create the output file?"

def test_duplicates_log_contents():
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"The file {log_path} is missing, cannot verify correctness."

    with open(log_path, "r") as f:
        log_lines = f.readlines()

    # Extract paths based on the exact format specified
    pattern = re.compile(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] \[INFO\] Deployed config to (.+)")

    extracted_paths = []
    for line in log_lines:
        match = pattern.match(line.strip())
        if match:
            extracted_paths.append(match.group(1).strip())

    unique_files = []
    expected_duplicates = []

    # Process files in order and find duplicates
    for path in extracted_paths:
        assert os.path.isfile(path), f"Extracted path {path} from deploy.log does not exist."
        with open(path, "r") as f:
            content = f.read()

        is_duplicate = False
        for unique_content in unique_files:
            ratio = difflib.SequenceMatcher(None, content, unique_content).ratio()
            if ratio >= 0.90:
                is_duplicate = True
                break

        if is_duplicate:
            expected_duplicates.append(path)
        else:
            unique_files.append(content)

    # Read the student's output
    duplicates_log_path = "/home/user/duplicates.log"
    assert os.path.isfile(duplicates_log_path), f"{duplicates_log_path} is missing."

    with open(duplicates_log_path, "r") as f:
        actual_duplicates = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_duplicates == expected_duplicates, (
        f"The contents of {duplicates_log_path} do not match the expected duplicate files.\n"
        f"Expected: {expected_duplicates}\n"
        f"Found: {actual_duplicates}"
    )