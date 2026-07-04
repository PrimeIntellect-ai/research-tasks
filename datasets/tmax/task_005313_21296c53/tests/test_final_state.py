# test_final_state.py

import os
import subprocess
import glob

def test_detector_exists():
    assert os.path.isfile('/home/user/detector.py'), "/home/user/detector.py does not exist."

def test_adversarial_corpus():
    detector_path = '/home/user/detector.py'

    clean_dir = '/home/user/corpora/clean'
    evil_dir = '/home/user/corpora/evil'

    clean_files = glob.glob(os.path.join(clean_dir, '*.csv'))
    evil_files = glob.glob(os.path.join(evil_dir, '*.csv'))

    assert len(clean_files) > 0, f"No clean CSV files found in {clean_dir}."
    assert len(evil_files) > 0, f"No evil CSV files found in {evil_dir}."

    clean_failures = []
    for cf in clean_files:
        try:
            result = subprocess.run(
                ['python3', detector_path, cf],
                capture_output=True,
                text=True,
                timeout=15
            )
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_failures.append(os.path.basename(cf))
        except subprocess.TimeoutExpired:
            clean_failures.append(f"{os.path.basename(cf)} (TIMEOUT)")
        except Exception as e:
            clean_failures.append(f"{os.path.basename(cf)} (ERROR: {str(e)})")

    evil_failures = []
    for ef in evil_files:
        try:
            result = subprocess.run(
                ['python3', detector_path, ef],
                capture_output=True,
                text=True,
                timeout=15
            )
            output = result.stdout.strip()
            if output != "EVIL":
                evil_failures.append(os.path.basename(ef))
        except subprocess.TimeoutExpired:
            evil_failures.append(f"{os.path.basename(ef)} (TIMEOUT)")
        except Exception as e:
            evil_failures.append(f"{os.path.basename(ef)} (ERROR: {str(e)})")

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: " + ", ".join(evil_failures))
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified: " + ", ".join(clean_failures))

    if error_msgs:
        assert False, " | ".join(error_msgs)