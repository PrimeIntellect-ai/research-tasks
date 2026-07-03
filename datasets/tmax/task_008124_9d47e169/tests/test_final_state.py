# test_final_state.py

import os

def test_metric_file_exists_and_correct():
    file_path = "/home/user/metric.txt"

    # Check if file exists
    assert os.path.exists(file_path), f"File {file_path} is missing. The Rust program must create it."
    assert os.path.isfile(file_path), f"{file_path} is not a regular file."

    # Check content
    with open(file_path, "r") as f:
        actual_content = f.read().strip()

    expected_content = "2.8750"

    assert actual_content == expected_content, (
        f"The calculated metric in {file_path} is incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Actual: '{actual_content}'"
    )

def test_rust_project_exists():
    project_dir = "/home/user/artifact_tester"
    # Even if they didn't use Cargo, they should have written code somewhere, 
    # but the prompt specifically suggests creating a standard Cargo project at /home/user/artifact_tester.
    # However, to be robust, we'll just check that the metric file was successfully created with the right value.
    # We can optionally check for rust source code.
    rust_files_found = False
    for root, dirs, files in os.walk("/home/user"):
        if any(f.endswith(".rs") for f in files):
            rust_files_found = True
            break

    assert rust_files_found, "No Rust source code (*.rs) found in /home/user. You must write a Rust program."