# test_final_state.py
import os
import subprocess
import pytest

DETECTOR_SCRIPT = "/home/user/detector.py"
EVIL_CORPUS_DIR = "/opt/verifier/corpus/evil"
CLEAN_CORPUS_DIR = "/opt/verifier/corpus/clean"

def run_detector(input_dir, output_log):
    assert os.path.exists(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"
    result = subprocess.run(
        ["python3", DETECTOR_SCRIPT, input_dir, output_log],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Detector script failed with return code {result.returncode}.\nStderr: {result.stderr}"

def test_detector_evil_corpus(tmp_path):
    output_log = str(tmp_path / "evil_out.txt")
    run_detector(EVIL_CORPUS_DIR, output_log)

    assert os.path.exists(output_log), f"Output log not created: {output_log}"

    with open(output_log, "r") as f:
        flagged_files = set(line.strip() for line in f if line.strip())

    expected_evil_files = set(os.listdir(EVIL_CORPUS_DIR))

    missed_evil = expected_evil_files - flagged_files
    extra_evil = flagged_files - expected_evil_files

    error_msg = ""
    if missed_evil:
        error_msg += f"{len(missed_evil)} of {len(expected_evil_files)} evil bypassed (not flagged). Missing: {', '.join(sorted(missed_evil))}\n"
    if extra_evil:
        error_msg += f"Flagged non-existent files in evil corpus: {', '.join(sorted(extra_evil))}\n"

    assert not missed_evil and not extra_evil, error_msg

def test_detector_clean_corpus(tmp_path):
    output_log = str(tmp_path / "clean_out.txt")
    run_detector(CLEAN_CORPUS_DIR, output_log)

    if not os.path.exists(output_log):
        # If the file wasn't created, we can assume nothing was flagged.
        flagged_files = set()
    else:
        with open(output_log, "r") as f:
            flagged_files = set(line.strip() for line in f if line.strip())

    expected_clean_files = set(os.listdir(CLEAN_CORPUS_DIR))

    # Clean files should NOT be flagged.
    falsely_flagged = flagged_files.intersection(expected_clean_files)
    extra_flagged = flagged_files - expected_clean_files

    error_msg = ""
    if falsely_flagged:
        error_msg += f"{len(falsely_flagged)} of {len(expected_clean_files)} clean modified (falsely flagged). Offending: {', '.join(sorted(falsely_flagged))}\n"
    if extra_flagged:
        error_msg += f"Flagged non-existent files in clean corpus: {', '.join(sorted(extra_flagged))}\n"

    assert not falsely_flagged and not extra_flagged, error_msg