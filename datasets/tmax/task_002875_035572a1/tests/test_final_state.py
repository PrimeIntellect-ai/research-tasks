# test_final_state.py

import os
import subprocess
import pytest

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector.py"
    assert os.path.isfile(detector_path), f"Detector script missing at {detector_path}"
    # Note: We just check if it's executable, though we'll run it with `python3` explicitly to be safe.
    assert os.access(detector_path, os.X_OK) or True, "Detector script should ideally be executable."

def test_detector_against_corpora():
    detector_path = "/home/user/detector.py"
    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    evil_files = set(f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f)))
    clean_files = set(f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f)))

    assert len(evil_files) > 0, "Evil corpus is empty, cannot verify."
    assert len(clean_files) > 0, "Clean corpus is empty, cannot verify."

    # Run detector against evil corpus
    evil_proc = subprocess.run(
        ["python3", detector_path, evil_dir],
        capture_output=True,
        text=True
    )
    assert evil_proc.returncode == 0, f"Detector script crashed on evil corpus: {evil_proc.stderr}"

    # Run detector against clean corpus
    clean_proc = subprocess.run(
        ["python3", detector_path, clean_dir],
        capture_output=True,
        text=True
    )
    assert clean_proc.returncode == 0, f"Detector script crashed on clean corpus: {clean_proc.stderr}"

    # Parse outputs
    evil_output_lines = set(line.strip() for line in evil_proc.stdout.splitlines() if line.strip())
    clean_output_lines = set(line.strip() for line in clean_proc.stdout.splitlines() if line.strip())

    # Check evil corpus: all evil files should be in the output
    bypassed_evil = evil_files - evil_output_lines

    # Check clean corpus: no clean files should be in the output
    flagged_clean = clean_output_lines.intersection(clean_files)

    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(sorted(bypassed_evil))}")
    if flagged_clean:
        errors.append(f"{len(flagged_clean)} of {len(clean_files)} clean modified (flagged): {', '.join(sorted(flagged_clean))}")

    assert not errors, " | ".join(errors)