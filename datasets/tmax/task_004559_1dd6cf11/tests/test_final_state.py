# test_final_state.py

import os
import csv
import subprocess
import pytest

def test_video_metrics_csv():
    csv_path = "/home/user/video_metrics.csv"
    assert os.path.isfile(csv_path), f"Video metrics CSV is missing at {csv_path}"

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 6, f"Expected at least a header and 5 rows, got {len(rows)} rows"

    header = rows[0]
    assert header == ["frame_number", "avg_intensity"], f"Incorrect CSV header: {header}"

    expected_intensities = [255, 0, 128, 64, 192]

    for i, expected in enumerate(expected_intensities):
        try:
            frame_num = int(rows[i+1][0])
            intensity = int(rows[i+1][1])
        except ValueError:
            pytest.fail(f"Row {i+2} contains non-integer values: {rows[i+1]}")

        assert frame_num == i + 1, f"Expected frame_number {i+1}, got {frame_num}"

        # Tolerate compression artifacts (e.g., YUV limited range shifts 0->16, 255->235)
        diff = abs(intensity - expected)
        assert diff <= 30, f"Frame {i+1} intensity {intensity} is too far from expected {expected} (diff: {diff})"

def test_meta_validator_adversarial_corpus():
    validator_bin = "/home/user/meta_validator"
    assert os.path.isfile(validator_bin), f"Validator binary missing at {validator_bin}"
    assert os.access(validator_bin, os.X_OK), f"Validator binary is not executable"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_modified = []
    evil_bypassed = []

    for cf in clean_files:
        result = subprocess.run([validator_bin, cf], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([validator_bin, ef], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))