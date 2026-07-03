# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_video_analysis_frames():
    output_file = "/home/user/deadlock_frames.txt"
    assert os.path.exists(output_file), f"Output file missing: {output_file}"

    with open(output_file, "r") as f:
        content = f.read().strip()

    # Split by comma, strip whitespace, and convert to integers
    try:
        frames = [int(x.strip()) for x in content.split(",") if x.strip()]
    except ValueError:
        pytest.fail(f"File {output_file} contains non-integer values: {content}")

    expected_frames = [24, 78, 142, 205, 310]
    assert frames == expected_frames, f"Expected frames {expected_frames}, but got {frames}"

def test_go_detector_evil_corpus():
    go_file = "/home/user/detector.go"
    assert os.path.exists(go_file), f"Go detector missing at {go_file}"

    evil_dir = "/app/corpus/evil/"
    evil_files = [os.path.basename(f) for f in glob.glob(os.path.join(evil_dir, "*.json"))]
    assert evil_files, f"No JSON files found in {evil_dir}"

    result = subprocess.run(["go", "run", go_file, evil_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Go program failed on evil corpus: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    missed_files = set(evil_files) - set(output_lines)
    assert not missed_files, f"{len(missed_files)} of {len(evil_files)} evil bypassed. Missed: {', '.join(missed_files)}"

def test_go_detector_clean_corpus():
    go_file = "/home/user/detector.go"
    assert os.path.exists(go_file), f"Go detector missing at {go_file}"

    clean_dir = "/app/corpus/clean/"
    clean_files = [os.path.basename(f) for f in glob.glob(os.path.join(clean_dir, "*.json"))]
    assert clean_files, f"No JSON files found in {clean_dir}"

    result = subprocess.run(["go", "run", go_file, clean_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Go program failed on clean corpus: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    flagged_files = set(clean_files).intersection(set(output_lines))
    assert not flagged_files, f"{len(flagged_files)} of {len(clean_files)} clean modified. Flagged: {', '.join(flagged_files)}"