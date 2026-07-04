# test_final_state.py
import os
import re
import subprocess

def test_bad_commit_hash():
    expected_path = "/tmp/expected_bad_commit.txt"
    actual_path = "/home/user/bad_commit_hash.txt"

    assert os.path.exists(expected_path), f"Expected bad commit file {expected_path} missing (test environment issue)"
    assert os.path.exists(actual_path), f"Student did not create {actual_path}"

    with open(expected_path, "r") as f:
        expected = f.read().strip()

    with open(actual_path, "r") as f:
        actual = f.read().strip()

    assert actual == expected, f"Expected bad commit hash '{expected}', but got '{actual}' in {actual_path}"

def test_make_success():
    repo_path = "/home/user/nightly_processor"
    binary_path = os.path.join(repo_path, "processor")

    # Remove binary if it exists to ensure make actually builds it
    if os.path.exists(binary_path):
        os.remove(binary_path)

    res = subprocess.run(["make"], cwd=repo_path, capture_output=True, text=True)
    assert res.returncode == 0, f"make failed with output:\n{res.stderr}\n{res.stdout}"
    assert os.path.exists(binary_path), "processor binary was not created by make"

def test_processor_does_not_hang():
    repo_path = "/home/user/nightly_processor"
    binary_path = os.path.join(repo_path, "processor")
    dataset_path = "/home/user/dataset.csv"

    assert os.path.exists(binary_path), "Processor binary not found. make must succeed first."

    try:
        # 2 seconds is more than enough for processing 4 lines
        res = subprocess.run([binary_path, dataset_path], capture_output=True, text=True, timeout=2)
        assert res.returncode == 0, f"Processor failed to run on dataset. Exit code: {res.returncode}\nStderr: {res.stderr}"
    except subprocess.TimeoutExpired:
        assert False, "Processor hung indefinitely on the dataset (infinite loop for negative numbers was not fixed)"

def test_report_generated():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"{report_path} was not generated"

    with open(report_path, "r") as f:
        content = f.read().strip()

    match = re.match(r"^PROCESSED_TOTAL:\s*(\d+)$", content)
    assert match is not None, f"Report content '{content}' does not match expected format 'PROCESSED_TOTAL:<int>'"