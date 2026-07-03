# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/telemetry_project"
RESULTS_FILE = os.path.join(PROJECT_DIR, "results.txt")

def test_results_file_exists():
    assert os.path.isfile(RESULTS_FILE), (
        f"The results file {RESULTS_FILE} does not exist. "
        "Did you successfully build the extension and run main.py?"
    )

def test_results_content():
    with open(RESULTS_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines of output in results.txt, found {len(lines)}."

    # Validate correct math calculation
    assert "27.5" in lines[0], f"Line 1 incorrect. Expected metric to be 27.5, got: {lines[0]}"
    assert "27.5" in lines[1], f"Line 2 incorrect. Expected metric to be 27.5, got: {lines[1]}"
    assert "27.5" in lines[3], f"Line 4 incorrect. Expected metric to be 27.5, got: {lines[3]}"

    # Validate bounds checking error handling
    assert lines[2].startswith("Error:"), (
        f"Line 3 incorrect. Expected an Error message for the malformed record, got: {lines[2]}"
    )

def test_fastparse_c_fixed():
    fastparse_path = os.path.join(PROJECT_DIR, "fastparse.c")
    assert os.path.isfile(fastparse_path), f"{fastparse_path} does not exist."

    with open(fastparse_path, "r") as f:
        content = f.read()

    # Check if bounds check is added
    assert "16" in content and (">" in content or ">=" in content or "<" in content), (
        "Could not find a bounds check for the payload length in fastparse.c. "
        "Ensure you check if the payload length exceeds 16."
    )
    assert "ValueError" in content, (
        "Ensure you raise a ValueError when the payload is too large."
    )

def test_main_py_fixed():
    main_path = os.path.join(PROJECT_DIR, "main.py")
    assert os.path.isfile(main_path), f"{main_path} does not exist."

    with open(main_path, "r") as f:
        content = f.read()

    assert "(velocity + wind_speed) * drag_coefficient / 2.0" in content.replace(" ", ""), (
        "The formula in main.py does not appear to be corrected properly. "
        "It should be: (velocity + wind_speed) * drag_coefficient / 2.0"
    )