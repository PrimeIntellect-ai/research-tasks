# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_filter_executable_exists():
    """Ensure the target executable exists and is executable."""
    target_executable = "/app/artifact-filter/filter"
    assert os.path.exists(target_executable), f"Target executable {target_executable} does not exist. Did you compile it?"
    assert os.access(target_executable, os.X_OK), f"Target executable {target_executable} is not executable."

def test_adversarial_corpus():
    """Test the filter against the clean and evil corpora."""
    target_executable = "/app/artifact-filter/filter"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.art"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.art"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for fpath in clean_files:
        try:
            result = subprocess.run([target_executable, fpath], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "ACCEPT":
                clean_failed.append((os.path.basename(fpath), output))
        except subprocess.TimeoutExpired:
            clean_failed.append((os.path.basename(fpath), "TIMEOUT (infinite loop?)"))
        except Exception as e:
            clean_failed.append((os.path.basename(fpath), f"ERROR: {str(e)}"))

    evil_failed = []
    for fpath in evil_files:
        try:
            result = subprocess.run([target_executable, fpath], capture_output=True, text=True, timeout=2)
            output = result.stdout.strip()
            if output != "REJECT":
                evil_failed.append((os.path.basename(fpath), output))
        except subprocess.TimeoutExpired:
            # A timeout could be considered a rejection, but the spec says "must print exactly REJECT"
            evil_failed.append((os.path.basename(fpath), "TIMEOUT (infinite loop?)"))
        except Exception as e:
            evil_failed.append((os.path.basename(fpath), f"ERROR: {str(e)}"))

    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed:")
        for fname, out in evil_failed:
            errors.append(f"  - {fname} (Output: {out})")

    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected:")
        for fname, out in clean_failed:
            errors.append(f"  - {fname} (Output: {out})")

    if errors:
        pytest.fail("\n".join(errors))