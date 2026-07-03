# test_final_state.py
import os
import subprocess
import pytest

def test_detector_clean_corpus():
    clean_dir = "/app/corpus/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
    assert len(clean_files) > 0, "No CSV files found in clean corpus"

    failed_files = []

    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run(
            ["python3", "/home/user/detector.py", filepath],
            capture_output=True, text=True
        )
        output = result.stdout.strip()
        if output != "ACCEPT":
            failed_files.append((filename, output))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected incorrectly.\n"
        error_msg += "Offending files:\n" + "\n".join(f"{f}: {out}" for f, out in failed_files)
        pytest.fail(error_msg)

def test_detector_evil_corpus():
    evil_dir = "/app/corpus/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]
    assert len(evil_files) > 0, "No CSV files found in evil corpus"

    failed_files = []

    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run(
            ["python3", "/home/user/detector.py", filepath],
            capture_output=True, text=True
        )
        output = result.stdout.strip()
        if output != "REJECT":
            failed_files.append((filename, output))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(evil_files)} evil files bypassed/accepted incorrectly.\n"
        error_msg += "Offending files:\n" + "\n".join(f"{f}: {out}" for f, out in failed_files)
        pytest.fail(error_msg)