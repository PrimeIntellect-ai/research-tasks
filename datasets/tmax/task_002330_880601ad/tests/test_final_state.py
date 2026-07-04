# test_final_state.py
import os
import subprocess
import tempfile
import pytest

def test_detector_adversarial_corpus():
    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"
    detector_script = "/home/user/detector.py"

    assert os.path.isfile(detector_script), f"Detector script not found at {detector_script}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    clean_modified = []
    evil_bypassed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test clean corpus
        for c_file in clean_files:
            out_file = os.path.join(tmpdir, os.path.basename(c_file))
            result = subprocess.run(["python3", detector_script, c_file, out_file], capture_output=True, text=True)
            if result.returncode != 0:
                clean_modified.append(f"{os.path.basename(c_file)} (script crashed)")
                continue

            if not os.path.exists(out_file):
                clean_modified.append(f"{os.path.basename(c_file)} (no output file)")
                continue

            with open(c_file, 'r') as f1, open(out_file, 'r') as f2:
                in_lines = f1.readlines()
                out_lines = f2.readlines()
                if in_lines != out_lines:
                    clean_modified.append(os.path.basename(c_file))

        # Test evil corpus
        for e_file in evil_files:
            out_file = os.path.join(tmpdir, os.path.basename(e_file))
            result = subprocess.run(["python3", detector_script, e_file, out_file], capture_output=True, text=True)
            if result.returncode != 0:
                evil_bypassed.append(f"{os.path.basename(e_file)} (script crashed)")
                continue

            if not os.path.exists(out_file):
                # Empty output is acceptable for evil (rejected all)
                continue

            with open(out_file, 'r') as f:
                out_lines = f.readlines()
                # Output should be completely empty or contain exactly one header line
                if len(out_lines) > 1:
                    evil_bypassed.append(os.path.basename(e_file))
                elif len(out_lines) == 1:
                    with open(e_file, 'r') as in_f:
                        in_header = in_f.readline()
                        if out_lines[0] != in_header:
                            evil_bypassed.append(os.path.basename(e_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))