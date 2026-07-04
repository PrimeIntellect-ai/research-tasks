# test_final_state.py

import os
import tarfile
import pytest
import shutil

TAR_PATH = "/app/final_backup.tar.gz"
EXTRACT_DIR = "/tmp/verify_final"
GO_CODE_PATH = "/app/archiver/main.go"

@pytest.fixture(scope="module", autouse=True)
def setup_extraction():
    assert os.path.exists(TAR_PATH), f"Tarball not found at {TAR_PATH}"

    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    with tarfile.open(TAR_PATH, "r:gz") as tar:
        tar.extractall(EXTRACT_DIR)

    yield

    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)

def test_tarball_contents():
    # Depending on how it was tarred, it might include the leading /app/archive_stage or archive_stage or just the files.
    # We will search for the two files recursively in the extracted directory.
    extracted_files = []
    for root, dirs, files in os.walk(EXTRACT_DIR):
        for f in files:
            extracted_files.append(f)

    assert "aggregated.log" in extracted_files, "aggregated.log not found in the extracted tarball."
    assert "light_frames.txt" in extracted_files, "light_frames.txt not found in the extracted tarball."

def get_extracted_file_path(filename):
    for root, dirs, files in os.walk(EXTRACT_DIR):
        if filename in files:
            return os.path.join(root, filename)
    return None

def test_aggregated_log():
    log_path = get_extracted_file_path("aggregated.log")
    assert log_path is not None, "aggregated.log is missing from tarball"

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    expected_lines = [
        "CRITICAL_BACKUP_FAILURE disk 0x1A",
        "CRITICAL_BACKUP_FAILURE network drop"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in aggregated.log"

    assert len(lines) == 2, f"aggregated.log should contain exactly 2 lines, found {len(lines)}"

def test_light_frames_metric():
    count_path = get_extracted_file_path("light_frames.txt")
    assert count_path is not None, "light_frames.txt is missing from tarball"

    with open(count_path, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"Content of light_frames.txt is not an integer: '{content}'"
    pred_count = int(content)

    ground_truth = 25
    error = abs(pred_count - ground_truth)
    assert error <= 2, f"Metric failed: Count error {error} exceeds threshold of 2 (Predicted: {pred_count}, Expected: {ground_truth})"

def test_go_code_atomic_write():
    assert os.path.exists(GO_CODE_PATH), f"Go source code not found at {GO_CODE_PATH}"

    with open(GO_CODE_PATH, "r", encoding="utf-8") as f:
        code = f.read()

    assert "os.Rename" in code or "Rename(" in code, "Atomic write pattern (Rename) missing in Go code."