# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_detector_exists():
    assert os.path.isfile("/home/user/detector.py"), "The script /home/user/detector.py does not exist."
    assert os.path.isfile("/home/user/DONE"), "The file /home/user/DONE does not exist."

def test_adversarial_corpus():
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert evil_files, f"No CSV files found in evil corpus dir: {evil_dir}"
    assert clean_files, f"No CSV files found in clean corpus dir: {clean_dir}"

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        try:
            result = subprocess.run(
                ["python3", "/home/user/detector.py", f],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout.strip()
            if output != "FRAUD":
                evil_bypassed.append((os.path.basename(f), output))
        except subprocess.TimeoutExpired:
            evil_bypassed.append((os.path.basename(f), "TIMEOUT"))
        except Exception as e:
            evil_bypassed.append((os.path.basename(f), f"ERROR: {str(e)}"))

    for f in clean_files:
        try:
            result = subprocess.run(
                ["python3", "/home/user/detector.py", f],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout.strip()
            if output != "NORMAL":
                clean_modified.append((os.path.basename(f), output))
        except subprocess.TimeoutExpired:
            clean_modified.append((os.path.basename(f), "TIMEOUT"))
        except Exception as e:
            clean_modified.append((os.path.basename(f), f"ERROR: {str(e)}"))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. Offending files: " + ", ".join([x[0] for x in evil_bypassed[:10]]))
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (flagged as FRAUD or error). Offending files: " + ", ".join([x[0] for x in clean_modified[:10]]))

    if error_msgs:
        pytest.fail("\n".join(error_msgs))